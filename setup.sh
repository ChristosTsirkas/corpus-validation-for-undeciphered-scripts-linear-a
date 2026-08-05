#!/usr/bin/env bash
# Fetch the external inputs the pipeline needs.
#
# NOTE: this script deliberately does NOT fetch the SigLA database. It is
# publicly served and openly licensed (CC BY-NC-SA 4.0), so retrieving it is
# lawful; but taking on a licence's obligations should be a knowing act, not a
# side effect. Use:  python3 src/extract_sigla.py --fetch
set -e

case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
        echo "This script does not support Windows."
        echo
        echo "mwenge/lineara.xyz (the Linear A corpus source) contains files"
        echo "whose names use characters (<, >, :, ?, \") that Windows/NTFS"
        echo "rejects outright - confirmed directly: even a plain 'git clone'"
        echo "of this repository fails on Windows with 'invalid path' errors"
        echo "for files this project's own code never reads. There is no"
        echo "reliable way to fetch this repository via a script on Windows"
        echo "without either those errors or silently losing data, so this"
        echo "script will not attempt it, and will not point elsewhere either."
        exit 1
        ;;
esac

echo "== dependencies =="
python3 -m pip install --quiet scipy beautifulsoup4

echo "== Linear A corpus (mwenge/lineara.xyz) =="
if [ ! -d raw_repo ]; then
    # Sparse checkout, not a full clone: this project's own code only ever
    # reads two things from this repo - LinearAInscriptions.js
    # (src/extract_raw.js) and commentary/ (src/parse_younger.py,
    # src/parse_younger_freetext.py). Everything else (images/, papers/,
    # network/, assets/, etc.) is never read by anything here, so there is
    # no reason to transfer it - smaller download (~12 MB against ~500 MB
    # for a full clone), and images/ in particular is very likely the same
    # GORILA plate photography this project's own licensing already states
    # is "not redistributed" (data/README.md item 7) - a full clone would
    # have pulled it onto the user's machine regardless of whether this
    # project's own code ever read it.
    git clone --filter=blob:none --no-checkout --depth 1 \
        https://github.com/mwenge/lineara.xyz.git raw_repo
    (
        cd raw_repo
        git sparse-checkout init --no-cone
        # A handful of commentary/ files have characters (<, >, :, ?, ")
        # illegal in Windows filenames - not a problem here (Windows is
        # blocked above, before this ever runs), but git itself still
        # excludes them from a plain sparse-checkout pattern match, so they
        # are recovered individually below rather than simply dropped.
        # Written with printf, one line at a time, rather than a heredoc: a
        # heredoc's closing marker silently fails to match if this file is
        # ever saved/checked-out with CRLF line endings, which swallows
        # everything after it as literal heredoc text instead of running it.
        printf '%s\n' \
            '/LinearAInscriptions.js' \
            '/commentary/*' \
            '!/commentary/*[<>:"|?*]*' \
            > .git/info/sparse-checkout
        git checkout -q

        echo "== recovering commentary files with special characters =="
        # Computed dynamically by diffing the full remote tree listing
        # against what's actually on disk - not a hardcoded list. Robust to
        # upstream adding more such files later: whatever the
        # sparse-checkout pattern above excluded is exactly what this finds
        # and fetches, today or in the future, without this script needing
        # an update either way.
        branch=$(git rev-parse --abbrev-ref origin/HEAD)
        BASE="https://raw.githubusercontent.com/mwenge/lineara.xyz/${branch#origin/}/commentary"
        comm -23 \
            <(git ls-tree -r --name-only "$branch" -- commentary/ | sort) \
            <(find commentary -type f | sort) |
        while IFS= read -r relpath; do
            name="${relpath#commentary/}"
            enc=$(python3 -c "
from urllib.parse import quote
import sys
print(quote(sys.argv[1], safe='()+.[]'))" "$name")
            curl -g -sL -o "commentary/$enc" "$BASE/$enc"
        done
    )
fi

echo "== Linear B lexicon (Luo, Cao & Barzilay 2019) =="
[ -d nd ] || git clone --depth 1 https://github.com/j-luo93/NeuroDecipher.git nd

echo
echo "Setup complete. Run the pipeline with:  ./src/run_all.sh"
echo
echo "Optional: to reproduce the SigLA-dependent results (sweep 3, the D4"
echo "correction, D12, the D8/D10 triage):"
echo
echo "    python3 src/extract_sigla.py --fetch"
echo
echo "That downloads SigLA's publicly served database.js under its CC BY-NC-SA 4.0"
echo "licence, caches it locally, and decodes it. Opt-in by design: read the"
echo "licence obligations it prints before taking them on."
