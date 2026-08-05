#!/usr/bin/env python3
"""
Shared file-reading helpers.

Exists so that the two-line pattern for reading JSON and text is defined once
rather than duplicated across every pipeline stage. Both close their handle
explicitly, which Python 3.12 and later warn about otherwise.

Every stage in `src/` is runnable standalone from the repository root, so this
module is imported by path rather than as a package.
"""
import json
import os
import sys
from typing import Any

# Allow `import corpus_io` from a stage run as `python3 src/<stage>.py`.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def json_load(path) -> Any:
    """Read and parse a JSON file, closing the handle."""
    with open(path, encoding='utf-8') as handle:
        data = json.load(handle)
    return data


def json_dump(obj, path, indent=None) -> str:
    """Write an object as UTF-8 JSON, creating the directory if needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(obj, handle, ensure_ascii=False, indent=indent)
    return path


def read_text(path) -> str:
    """Read a text file as UTF-8, closing the handle."""
    with open(path, encoding='utf-8') as handle:
        text = handle.read()
    return text
