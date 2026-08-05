#!/usr/bin/env python3
"""
Sweep 2, step A: parse Younger's NON-TABULAR commentary records.

Layout:
  <dt>            header / physical description        -> skip
  <dd>            transliteration line                 -> parse
  <dd><font red>  editorial commentary                 -> skip
  <dd><img>       layout illustration                  -> skip

Younger's conventions inside a transliteration line:
  <u>SIGN</u>   the reading of SIGN is doubtful   -> captured as `doubtful`
  •             word divider
  [ ]           break / restoration
  [•] or -•-    unidentified sign

Line labels are '.1:' (lines) or 'a:'..'d:' (facets of a libation table).
Facet labels are NOT recto/verso sides and must not be used to split records.
"""
import os, re, json, glob
from urllib.parse import unquote
from typing import TypedDict
from bs4 import BeautifulSoup
from bs4.element import NavigableString


class FreetextLine(TypedDict):
    label: str | None
    text: str


class FreetextToken(TypedDict):
    val: str
    line: str | None
    doubtful: bool
    break_before: bool
    break_after: bool


SRC = 'raw_repo/commentary'
LINE_LABEL = re.compile(r'^\s*((?:[a-z]|\.\d+|[a-z]\.\d+)\s*:)\s*')
EDITORIAL_WORDS = re.compile(
    r'\b(GORILA|JGY|probably|photograph|scratches|excluded|reads|says)\b', re.I)


def read_text_lenient(path, encoding='utf-8', errors='replace') -> str:
    with open(path, encoding=encoding, errors=errors) as f:
        return f.read()


SEAL_RE = re.compile(r'seal impression|CMS\b', re.I)


def _render(node) -> str:
    """Render a node to text, dropping commentary and marking doubtful signs.

    The scraped HTML has malformed nesting: some red-font tags WRAP black-font
    content instead of being commentary. A red font that contains a black font
    is therefore treated as a wrapper and recursed into; one that does not is
    genuine editorial commentary and is dropped.
    """
    if isinstance(node, NavigableString):
        return str(node)
    name = getattr(node, 'name', None)
    if name in ('img', 'h2', 'center', 'table'):
        return ''
    if name == 'font' and node.get('color') == 'red':
        if node.find('font', color='black') is None:
            return ''
    if name == 'sub':
        return node.get_text().strip()
    if name == 'u':
        return '~' + node.get_text().strip() + '~'
    return ''.join(_render(c) for c in node.children)


def dd_text(dd) -> str:
    txt = _render(dd)
    txt = txt.replace('\xa0', ' ')
    txt = re.sub(r'\s+', ' ', txt)
    txt = re.sub(r'\s*-\s*', '-', txt)
    txt = re.sub(r'~\s+', '~', txt)
    txt = re.sub(r'\s+~', '~', txt)
    txt = re.sub(r'(?<=[A-Z0-9])\s+(?=\d\b)', '', txt)
    return txt.strip()


def parse_file(path) -> list[FreetextLine] | None:
    soup = BeautifulSoup(read_text_lenient(path, encoding='utf-8', errors='replace'),
                         'html.parser')
    if soup.find('table') is not None:
        return None                      # tabular: handled by sweep 1
    lines = []
    for dd in soup.find_all('dd'):
        txt = dd_text(dd)
        if not txt:
            continue
        m = LINE_LABEL.match(txt)
        label = m.group(1).rstrip(':').strip() if m else None
        if m:
            txt = txt[m.end():]
        if SEAL_RE.search(txt) or EDITORIAL_WORDS.search(txt):
            continue                     # stray prose that escaped the red font
        # Younger's transliteration is upper-case; a line dominated by
        # lower-case letters is prose (physical description, find-context).
        alpha = [c for c in txt if c.isalpha()]
        if alpha and sum(c.islower() for c in alpha) / len(alpha) > 0.20:
            continue
        if not txt.strip():
            continue
        lines.append({'label': label, 'text': txt.strip()})
    return lines if lines else None


def tokenise(lines) -> list[FreetextToken]:
    toks = []
    for ln in lines:
        for part in re.split(r'[•·]', ln['text']):
            part = part.strip()
            if not part:
                continue
            for piece in part.split():
                doubtful = '~' in piece
                val = piece.replace('~', '')
                # break brackets recorded separately, not part of the sign string
                brk_before = val.startswith(']') or ']' in val.split('-')[0]
                brk_after = val.endswith('[') or val.endswith('[]')
                val = val.replace('[', '').replace(']', '')
                val = val.strip('-')
                if not val or val in {'.', ','}:
                    continue
                if re.fullmatch(r'[a-z0-9.\-]{1,6}:', val):
                    continue          # stray facet/line label (e.g. 'b-c:')
                val = re.sub(r'^[a-z0-9.\-]{1,6}:', '', val)
                toks.append({'val': val, 'line': ln['label'],
                             'doubtful': doubtful,
                             'break_before': brk_before,
                             'break_after': brk_after})
    return toks


def main() -> None:
    out, n = {}, 0
    files = sorted(glob.glob(os.path.join(SRC, '*.html')))
    for f in files:
        lines = parse_file(f)
        if not lines:
            continue
        toks = tokenise(lines)
        if not toks:
            continue
        # unquote(): see the matching comment in parse_younger.py - recovers
        # the true filename for the ~20 commentary files setup.sh saves
        # percent-encoded. No-op for every other filename.
        out[unquote(os.path.basename(f)[:-5])] = toks
        n += 1
    with open('data/younger_freetext.json', 'w', encoding='utf-8') as _f:
        json.dump(out, _f,
              ensure_ascii=False, indent=1)
    print(f'files scanned            : {len(files)}')
    print(f'non-tabular records kept : {n}')
    print(f'tokens                   : {sum(len(v) for v in out.values())}')
    print(f'doubtful signs flagged   : {sum(1 for v in out.values() for t in v if t["doubtful"])}')


if __name__ == '__main__':
    main()
