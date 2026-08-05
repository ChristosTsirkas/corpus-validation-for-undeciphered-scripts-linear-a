#!/usr/bin/env python3
"""
Sweep 1, step A: parse Younger's commentary tables into token sequences.

Columns: side.line | statement | logogram | number | fraction
Reading order per row: statement -> logogram -> number -> fraction.
Whitespace inside a cell is HTML line-wrap noise and is removed.
Sides (a/b) are taken from the line column so records can be matched to ours.
"""
import os, re, json, glob
from urllib.parse import unquote
from typing import Literal, Optional, TypedDict, Union
from bs4 import BeautifulSoup


class YoungerRow(TypedDict):
    line: str
    statement: str
    logogram: str
    number: str
    fraction: str


class YoungerToken(TypedDict):
    val: str
    col: str
    line: str
    side: str | None
    erased: bool


def read_text_lenient(path, encoding='utf-8', errors='replace') -> str:
    with open(path, encoding=encoding, errors=errors) as f:
        return f.read()


SRC = 'raw_repo/commentary'
# Younger's editorial apparatus. Not tokens on the tablet.
SKIP = {'vacat', 'vacant', 'vacats', 'deest', 'deesunt', 'desunt',
        'supramutila', 'inframutila', 'vest.', 'vest', 'vestigia',
        'mutila', 'lacuna', ''}

# Roundel/sealing tables use a different schema (seal impressions, CMS numbers)
# and are not sign tables. Detected by header and excluded.
NON_SIGN_HEADERS = {'no.ofimpressions', 'cmsno.', 'cmsno', 'sealimpression'}

def clean_cell(s) -> str:
    s = s.replace('\xa0', ' ')
    s = re.sub(r'\{[^}]*\}', '', s)     # Younger's {*684} sign-number glosses
    s = re.sub(r'\s+', '', s)           # intra-cell whitespace is markup noise
    return s.strip()

def parse_file(path) -> Optional[Union[list[YoungerRow], Literal['NONSIGN']]]:
    soup = BeautifulSoup(read_text_lenient(path, encoding='utf-8', errors='replace'),
                         'html.parser')
    table = soup.find('table')
    if table is None:
        return None
    header, rows = None, []
    for tr in table.find_all('tr'):
        cells = [td.get_text() for td in tr.find_all('td')]
        if not cells:
            continue
        norm = [re.sub(r'[\s"\u201c\u201d\u2018\u2019\']', '', c).lower()
                for c in cells]
        if header is None and 'statement' in norm:
            if set(norm) & NON_SIGN_HEADERS:
                return 'NONSIGN'          # roundel/sealing schema, not a sign table
            header = norm
            continue
        if header is None:
            continue
        cells = [clean_cell(c) for c in cells]
        row = dict(zip(header, cells))
        rows.append({
            'line':      row.get('side.line', ''),
            'statement': row.get('statement', ''),
            'logogram':  row.get('logogram', ''),
            'number':    row.get('number', ''),
            'fraction':  row.get('fraction', ''),
        })
    return rows if rows else None


def side_of(line) -> str | None:
    m = re.match(r'^([ab])\.', line or '')
    return m.group(1) if m else None

def rows_to_tokens(rows) -> list[YoungerToken]:
    toks = []
    for r in rows:
        side = side_of(r['line'])
        for col in ('statement', 'logogram', 'number', 'fraction'):
            v = r[col]
            if not v or v.lower() in SKIP:
                continue
            for part in re.split(r'•', v):
                part = part.strip()
                if not part or part.lower() in SKIP:
                    continue
                erased = '[[' in part or ']]' in part
                val = part.replace('[[', '').replace(']]', '')
                if not val or val.lower() in SKIP:
                    continue
                toks.append({'val': val, 'col': col,
                             'line': r['line'], 'side': side,
                             'erased': erased})
    return toks

def main() -> None:
    out, tabular, nonsign = {}, 0, 0
    files = sorted(glob.glob(os.path.join(SRC, '*.html')))
    for f in files:
        rows = parse_file(f)
        if rows is None:
            continue
        if rows == 'NONSIGN':
            nonsign += 1
            continue
        # unquote(): setup.sh saves the ~20 commentary files with characters
        # (<, >, :, ?, ") illegal in Windows filenames under percent-encoded
        # names (e.g. 'PH(%3F)31.html'), so the sparse-checkout pattern that
        # excludes them can recover them individually afterward. Decoding
        # here recovers the true key so those ~20 records are keyed
        # identically to every other file - a no-op for the other ~1716
        # filenames, which contain no % sequences.
        out[unquote(os.path.basename(f)[:-5])] = rows_to_tokens(rows)
        tabular += 1
    with open('data/younger_tokens.json', 'w', encoding='utf-8') as _f:
        json.dump(out, _f,
              ensure_ascii=False, indent=1)
    sided = sum(1 for v in out.values() if any(t['side'] for t in v))
    print(f'commentary files scanned : {len(files)}')
    print(f'tabular records parsed   : {tabular}  (of which two-sided: {sided})')
    print(f'non-sign tables excluded : {nonsign}')
    print(f'total Younger tokens     : {sum(len(v) for v in out.values())}')
    print(f'erased tokens flagged    : {sum(1 for v in out.values() for t in v if t["erased"])}')

if __name__ == '__main__':
    main()
