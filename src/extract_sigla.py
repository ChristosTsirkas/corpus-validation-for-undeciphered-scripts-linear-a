#!/usr/bin/env python3
"""
Extract the SigLA corpus from database.js into JSON.

Record layout, recovered by structural analysis of the marshaled data and
cross-checked against sigil/import/importer.ml:

document map: name -> B0[1]( B0[5]( meta, path, ..., dims, attestations ) )
  meta        = B0[ kind, name, site, _, _, _, dims, period, gorila_url, ... ]
  attestation = B0[8](
      f0 sign-ref block
      f1 label   : 0 = unreadable/unclassified
                   B0[ B0[ sign, variant ], confidence ]   confidence 1|0
      f2 number  : occurrence index within the document
      f3 bounds  : word-boundary state (see below)
      f4 flag    : 104 set    (erasure)
      f5 flag    : 0 set
      f6 flag    : 7 set      (ghost)
      f7 bbox    : 4 ints
  )
  sign        = B0[ series, number, values, ref, ... ]   e.g. ['AB', 1, ['da'], 'PH 31a/17']

`confidence` is the field that D12 requires: our corpus cannot distinguish a
doubtful reading from a confident one, because the marking is absent from every
layer of its source. SigLA carries it natively.
"""
import sys, os, json, argparse, collections, hashlib, urllib.request
from collections.abc import Iterator
from typing import TypedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ocaml_marshal import load, Block, MarshalValue


class SignInfo(TypedDict):
    """Unpacked sign block: series/number/sign_id/values/reference.

    series, number and reference are decoded OCaml Marshal fields, which are
    dynamically typed in general (see ocaml_marshal.MarshalValue); in every
    attestation this project has seen they resolve to str, int and str|None
    respectively, so those are the practical types used here.
    """
    series: str
    number: int
    sign_id: str | None
    values: list[str]
    reference: str | None


def read_bytes(path, mode='rb') -> bytes:
    with open(path, mode) as f:
        return f.read()



def walk_map(v: 'MarshalValue | None') -> Iterator[tuple['MarshalValue | None', 'MarshalValue | None']]:
    """OCaml Map.t is a balanced tree: B0[left, key, value, right, height].

    Generic over whatever the map's keys and values are; this file's only use
    (the SigLA document map: name -> wrapped document Block) narrows the
    yielded pairs at the call site, since a Map.t in general carries no
    guarantee about what its keys and values are.
    """
    if v == 0 or not isinstance(v, Block) or len(v.fields) != 5:
        return
    yield from walk_map(v.fields[0])
    yield v.fields[1], v.fields[2]
    yield from walk_map(v.fields[3])


def sign_of(b: 'MarshalValue | None') -> SignInfo | None:
    """Unpack a sign block to (id, values, reference)."""
    if not isinstance(b, Block) or len(b.fields) < 4:
        return None
    series, num, vals, ref = b.fields[0], b.fields[1], b.fields[2], b.fields[3]
    if not isinstance(series, str) or not isinstance(num, int):
        return None          # not the shape a sign block is documented to have
    values: list[str] = []
    if isinstance(vals, Block):
        for v in vals.fields:
            if isinstance(v, Block) and v.fields:
                v0 = v.fields[0]
                if isinstance(v0, str):
                    values.append(v0)
    ref0 = ref.fields[0] if isinstance(ref, Block) and ref.fields else None
    reference = ref0 if isinstance(ref0, str) else None
    return SignInfo(series=series, number=num,
                     sign_id=f'{series}{num:03d}',
                     values=values, reference=reference)


def label_of(f1: 'MarshalValue | None') -> tuple[SignInfo | None, bool | None]:
    """f1 -> (sign dict | None, confident: bool | None).

    f1 is 0 when the attestation is unreadable or unclassified, and a
    two-field Block otherwise.
    """
    if isinstance(f1, Block) and len(f1.fields) == 2:
        inner, conf = f1.fields
        if isinstance(inner, Block) and inner.fields:
            return sign_of(inner.fields[0]), bool(conf)
    return None, None


def bounds_of(f3: 'MarshalValue | None') -> dict[str, int] | dict[str, str]:
    """Word-boundary state. importer.ml: Bound.t = Here | Unsure | Not_here."""
    def norm(x: 'MarshalValue | None') -> dict[str, int] | dict[str, str]:
        if isinstance(x, Block) and len(x.fields) == 2:
            start, end = x.fields[0], x.fields[1]
            if isinstance(start, int) and isinstance(end, int):
                return {'start': start, 'end': end}
        return {'raw': repr(x)[:40]}
    if isinstance(f3, Block):
        if len(f3.fields) == 2 and isinstance(f3.fields[0], Block):
            return norm(f3.fields[0])
        return norm(f3)
    return {'raw': repr(f3)[:40]}


SIGLA_URL = 'https://sigla.phis.me/database.js'
LICENCE_NOTICE = """
  SigLA dataset (c) 2020- Ester Salgarella and Simon Castellan.
  Licensed CC BY-NC-SA 4.0.  https://sigla.phis.me/

  By fetching this file you take on the licence obligations:
    * attribute Salgarella and Castellan
    * non-commercial use only
    * share alike: any derivative you distribute carries the same terms

  Cite: Salgarella, E. & Castellan, S. (2021), "SigLA: The Signs of Linear A.
  A Paleographical Database", Proc. 5th Int. Conf. on Digital Access to
  Textual Cultural Heritage.
"""


def fetch(url, dest) -> str:
    """Download database.js once and cache it.

    The file is publicly served without authentication and the dataset carries
    an explicit CC BY-NC-SA 4.0 grant, so retrieving it is ordinary licensed
    use. It is cached rather than re-fetched so that repeated pipeline runs do
    not repeatedly hit an academic project's server.
    """
    if os.path.exists(dest):
        print(f'using cached {dest} ({os.path.getsize(dest)//1024} KB)')
        return dest
    print(LICENCE_NOTICE)
    print(f'fetching {url}')
    os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
    req = urllib.request.Request(
        url, headers={'User-Agent': 'linear-a-audit/1.0 (academic, non-commercial)'})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, 'wb') as f:
        f.write(r.read())
    print(f'cached at {dest} ({os.path.getsize(dest)//1024} KB)')
    return dest


def main() -> None:
    ap = argparse.ArgumentParser(
        description='Extract the SigLA corpus to JSON.',
        epilog='SigLA data is CC BY-NC-SA 4.0 (Salgarella & Castellan). '
               'Attribute, non-commercial, share alike.')
    ap.add_argument('--input', default='data/database.js',
                    help='path to SigLA database.js (default: data/database.js)')
    ap.add_argument('--output', default='data/sigla_corpus.json')
    ap.add_argument('--fetch', action='store_true',
                    help='download database.js from sigla.phis.me if absent, '
                         'and cache it at --input. Opt-in: retrieving another '
                         "project's data should be a deliberate act.")
    args = ap.parse_args()

    if args.fetch:
        try:
            fetch(SIGLA_URL, args.input)
        except Exception as e:
            print(f'fetch failed: {e}')
            print('Obtain database.js manually, or see data/README.md.')
            return

    if not os.path.exists(args.input):
        print(f'SigLA database.js not found at {args.input!r}.')
        print()
        print('  Run again with --fetch to download it from sigla.phis.me,')
        print('  or place the file at that path yourself.')
        print()
        print('  The dataset is CC BY-NC-SA 4.0; see data/README.md item 3.')
        print('  Skipping SigLA-dependent stages.')
        return

    d = load(args.input)
    data_blob = d['data']
    assert isinstance(data_blob, Block), (
        f'unexpected top-level shape for the data blob: {type(data_blob).__name__}')
    root = data_blob.fields[0]
    docs = dict(walk_map(root))

    out = []
    stats = collections.Counter()
    for name, wrap in docs.items():
        if not isinstance(name, str) or not isinstance(wrap, Block) or not wrap.fields:
            continue
        inner = wrap.fields[0]
        if not isinstance(inner, Block) or not inner.fields:
            continue
        meta = inner.fields[0]
        kind = meta.fields[0] if isinstance(meta, Block) else None
        site = meta.fields[2] if isinstance(meta, Block) and len(meta.fields) > 2 else None
        period = None
        if isinstance(meta, Block) and len(meta.fields) > 7 and isinstance(meta.fields[7], Block):
            period_block = meta.fields[7]
            if isinstance(period_block, Block) and period_block.fields:
                period = period_block.fields[0]

        atts = []
        arr = inner.fields[4] if len(inner.fields) > 4 else None
        if isinstance(arr, Block):
            for a in arr.fields:
                if not (isinstance(a, Block) and len(a.fields) == 8):
                    continue
                sign, conf = label_of(a.fields[1])
                rec = {
                    'n': a.fields[2],
                    'sign_id': sign['sign_id'] if sign else None,
                    'values': sign['values'] if sign else [],
                    'confident': conf,
                    'bounds': bounds_of(a.fields[3]),
                    'erasure': bool(a.fields[4]),
                    'flag5': bool(a.fields[5]),
                    'ghost': bool(a.fields[6]),
                }
                atts.append(rec)
                stats['attestations'] += 1
                if conf is None:
                    stats['unreadable_or_unclassified'] += 1
                elif conf:
                    stats['confident'] += 1
                else:
                    stats['DOUBTFUL'] += 1
                if rec['erasure']:
                    stats['erasure'] += 1
                if rec['ghost']:
                    stats['ghost'] += 1

        out.append({'name': name, 'kind': kind, 'site': site,
                    'period': period, 'attestations': atts})
        stats['documents'] += 1

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as _f:
        json.dump(out, _f, ensure_ascii=False)
    md5 = hashlib.md5(read_bytes(args.output, 'rb')).hexdigest()
    print('=== SigLA extraction ===')
    for k in sorted(stats):
        print(f'  {str(k):28s} {stats[k]}')
    print(f'  {"md5":28s} {md5}')
    if md5 != 'f3cb6d5805bd5376eef7099705d3d2ef':
        print('  NOTE: differs from the snapshot used for the paper. SigLA has')
        print('        been updated since; expected over time, not an error.')
    print()
    print('  Output derives from SigLA and remains CC BY-NC-SA 4.0.')
    print('  Attribute Salgarella & Castellan; non-commercial; share alike.')


if __name__ == '__main__':
    main()
