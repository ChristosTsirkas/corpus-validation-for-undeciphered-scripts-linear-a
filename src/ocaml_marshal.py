#!/usr/bin/env python3
"""
Parser for OCaml's Marshal binary format, as used by SigLA's database.js.

SigLA ships its corpus as two OCaml `Marshal` blobs escaped as decimal octets
inside JavaScript string literals. OCaml marshal stores records POSITIONALLY -
no field names - which is why grepping for `unsure` finds nothing even though
the value is present. Decoding requires implementing the format.

Format reference: OCaml runtime intext.h / extern.c.
  header: magic 0x8495A6BE, data_len, num_objects, size_32, size_64 (20 bytes)
  values:
    0x00-0x3F  : 0x00 INT8, 0x01 INT16, 0x02 INT32, 0x03 INT64,
                 0x04 SHARED8, 0x05 SHARED16, 0x06 SHARED32,
                 0x08 BLOCK32, 0x09 STRING8, 0x0A STRING32,
                 0x0B DOUBLE_BIG, 0x0C DOUBLE_LITTLE, 0x12 CUSTOM,
                 0x13 BLOCK64, 0x14 SHARED64, 0x15 STRING64,
                 0x20-0x3F PREFIX_SMALL_STRING (len = b & 0x1F)
    0x40-0x7F  : PREFIX_SMALL_INT   (value = b & 0x3F)
    0x80-0xFF  : PREFIX_SMALL_BLOCK (tag = b & 0x0F, size = (b >> 4) & 0x07)

Sharing: OCaml emits back-references to previously written objects, so the
parser must keep an ordered table of every block and string it creates.
"""
from __future__ import annotations
import struct, re
from typing import cast


def read_text_lenient(path, encoding='utf-8', errors='replace') -> str:
    with open(path, encoding=encoding, errors=errors) as f:
        return f.read()



class Block:
    __slots__ = ('tag', 'fields')

    def __init__(self, tag: int, fields: list[MarshalValue | None]) -> None:
        self.tag = tag
        self.fields = fields

    def __repr__(self) -> str:
        return f'Block(tag={self.tag}, {self.fields!r})'


# A decoded OCaml Marshal value. Genuinely a union at runtime - which OCaml
# constructor was serialized determines which of these comes back - so this
# is a real type, not a stand-in for an unannotated Any.
MarshalValue = Block | int | str | float | list[float]


class Unmarshal:
    def __init__(self, buf, off=0) -> None:
        self.b = buf
        self.i = off
        self.objs = []          # sharing table

    # --- primitive readers ------------------------------------------------
    def u8(self) -> int:
        v = self.b[self.i]; self.i += 1; return v

    def u16(self) -> int:
        v = struct.unpack_from('>H', self.b, self.i)[0]; self.i += 2; return v

    def u32(self) -> int:
        v = struct.unpack_from('>I', self.b, self.i)[0]; self.i += 4; return v

    def i8(self) -> int:
        v = struct.unpack_from('>b', self.b, self.i)[0]; self.i += 1; return v

    def i16(self) -> int:
        v = struct.unpack_from('>h', self.b, self.i)[0]; self.i += 2; return v

    def i32(self) -> int:
        v = struct.unpack_from('>i', self.b, self.i)[0]; self.i += 4; return v

    def i64(self) -> int:
        v = struct.unpack_from('>q', self.b, self.i)[0]; self.i += 8; return v

    def string(self, n) -> str:
        s = self.b[self.i:self.i + n]; self.i += n
        return s.decode('utf-8', 'replace')

    # --- header -----------------------------------------------------------
    def header(self) -> tuple[int, int]:
        magic = self.u32()
        if magic != 0x8495A6BE:
            raise ValueError(f'bad magic {magic:#x}')
        data_len = self.u32()
        num_objects = self.u32()
        self.u32(); self.u32()          # size_32, size_64
        return data_len, num_objects

    # --- value ------------------------------------------------------------
    def value(self) -> MarshalValue:
        code = self.u8()

        if code >= 0x80:                                   # small block
            tag = code & 0x0F
            size = (code >> 4) & 0x07
            if size == 0:
                return Block(tag, [])
            fields = cast('list[MarshalValue | None]', [None] * size)
            blk = Block(tag, fields)
            self.objs.append(blk)
            for k in range(size):
                blk.fields[k] = self.value()
            return blk

        if code >= 0x40:                                   # small int
            return code & 0x3F

        if code >= 0x20:                                   # small string
            s = self.string(code & 0x1F)
            self.objs.append(s)
            return s

        if code == 0x00: return self.i8()
        if code == 0x01: return self.i16()
        if code == 0x02: return self.i32()
        if code == 0x03: return self.i64()

        if code == 0x04: return self.shared(self.u8())
        if code == 0x05: return self.shared(self.u16())
        if code == 0x06: return self.shared(self.u32())
        if code == 0x14: return self.shared(struct.unpack_from('>Q', self.b, self._adv(8))[0])

        if code == 0x08:                                   # block32
            hdr = self.u32()
            tag = hdr & 0xFF
            size = hdr >> 10
            if size == 0:
                return Block(tag, [])
            fields = cast('list[MarshalValue | None]', [None] * size)
            blk = Block(tag, fields)
            self.objs.append(blk)
            for k in range(size):
                blk.fields[k] = self.value()
            return blk

        if code == 0x09:                                   # string8
            s = self.string(self.u8()); self.objs.append(s); return s
        if code == 0x0A:                                   # string32
            s = self.string(self.u32()); self.objs.append(s); return s

        if code == 0x0B:                                   # double, big endian
            v = struct.unpack_from('>d', self.b, self.i)[0]; self.i += 8
            self.objs.append(v); return v
        if code == 0x0C:                                   # double, little endian
            v = struct.unpack_from('<d', self.b, self.i)[0]; self.i += 8
            self.objs.append(v); return v

        if code == 0x0D or code == 0x0E:                   # double array 8
            n = self.u8()
            fmt = '>' if code == 0x0D else '<'
            arr = list(struct.unpack_from(fmt + 'd' * n, self.b, self.i))
            self.i += 8 * n; self.objs.append(arr); return arr
        if code == 0x07 or code == 0x0F:                   # double array 32
            n = self.u32()
            fmt = '>' if code == 0x0F else '<'
            arr = list(struct.unpack_from(fmt + 'd' * n, self.b, self.i))
            self.i += 8 * n; self.objs.append(arr); return arr

        if code == 0x12 or code == 0x18 or code == 0x19:   # custom
            j = self.b.index(b'\x00', self.i)
            ident = self.b[self.i:j].decode('ascii', 'replace')
            self.i = j + 1
            if ident in ('_i', '_j'):
                v = self.i32() if ident == '_i' else self.i64()
                self.objs.append(v); return v
            raise ValueError(f'unsupported custom {ident!r} at {self.i}')

        raise ValueError(f'unknown code {code:#x} at offset {self.i - 1}')

    def _adv(self, n) -> int:
        o = self.i; self.i += n; return o

    def shared(self, back) -> MarshalValue:
        return self.objs[len(self.objs) - back]


# ---------------------------------------------------------------- loading --
def unescape(body: str) -> bytes:
    out = bytearray()
    i, n = 0, len(body)
    while i < n:
        c = body[i]
        if c == '\\':
            j = i
            while j < n and body[j] == '\\':
                j += 1
            if j + 2 < n and body[j:j + 3].isdigit():
                out.append(int(body[j:j + 3]) & 0xFF)
                i = j + 3
                continue
            out.extend(b'\\' * ((j - i) // 2))
            i = j
            continue
        out.append(ord(c) & 0xFF)
        i += 1
    return bytes(out)


def load(path='database.js') -> dict[str, MarshalValue]:
    src = read_text_lenient(path, encoding='utf-8', errors='replace')
    out = {}
    for name in ('signs', 'data'):
        m = re.search(r"var\s+" + name + r"\s*=\s*'(.*?)';", src, re.S)
        if not m:
            continue
        raw = unescape(m.group(1))
        k = raw.find(b'\x84\x95\xa6\xbe')          # skip any leading quote
        u = Unmarshal(raw, k)
        u.header()
        out[name] = u.value()
    return out


def _demo() -> None:
    """Print a summary of each blob, for inspecting an unfamiliar file."""
    blobs = load()
    for name, value in blobs.items():
        print(f'=== {name}: {type(value).__name__} ===')
        print(repr(value)[:1200])
        print()


if __name__ == '__main__':
    _demo()
