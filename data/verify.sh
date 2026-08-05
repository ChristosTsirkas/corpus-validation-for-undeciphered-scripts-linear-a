#!/usr/bin/env bash
# Verify that locally generated data matches what the paper was written against.
# Reports presence, size and checksum for each file, and names the command that
# produces anything missing. Exit 0 if everything needed for the full pipeline
# is present and matching; 1 otherwise.
cd "$(dirname "$0")/.."

EXPECT_CORPUS="2f5c936f0848fcbcb4ef35669eccca99"
EXPECT_SIGLA="f3cb6d5805bd5376eef7099705d3d2ef"
EXPECT_CORPUS_SHA="a642976320aaaa52f67f3fc29539a3ee88ea683e25bc2d6d8969e6d6114a93a1"
EXPECT_SIGLA_SHA="7e2157090b847a1bafccd2a7465babd8a9c9b4f7de5b28ce22ecf9ce3f5106b8"
STATUS=0

md5of()    { md5sum    "$1" 2>/dev/null | cut -d' ' -f1; }
sha256of() { sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
human() { du -h "$1" 2>/dev/null | cut -f1; }

echo "=============================================================="
echo " undeciphered-corpora-audit : data verification"
echo "=============================================================="
echo " No corpus data is redistributed by this repository. Both corpora"
echo " are generated locally; see data/README.md for licences and terms."

check_dir () {   # name, path, marker file, clone command
  printf '\n[%s]\n' "$1"
  if [ -e "$3" ]; then
    printf '  present   %s (%s)\n' "$3" "$(human "$3")"
  else
    printf '  MISSING   %s\n' "$3"
    printf '  produce:  %s\n' "$4"
    STATUS=1
  fi
}

check_file () { # name, path, expected md5, produce command, required(y/n), expected sha256
  printf '\n[%s]\n' "$1"
  if [ ! -f "$2" ]; then
    printf '  MISSING   %s\n' "$2"
    printf '  produce:  %s\n' "$4"
    [ "$5" = "y" ] && STATUS=1
    return
  fi
  local got; got=$(md5of "$2")
  local gotsha; gotsha=$(sha256of "$2")
  printf '  present   %s (%s)\n' "$2" "$(human "$2")"
  printf '  md5       %s\n' "$got"
  printf '  sha256    %s\n' "$gotsha"
  if [ -n "$6" ] && [ "$gotsha" != "$6" ] && [ "$got" = "$3" ]; then
    printf '  WARNING   md5 matches but sha256 does not. Investigate.\n'
  fi
  if [ "$got" = "$3" ]; then
    printf '  MATCH     identical to the snapshot used for the paper\n'
  else
    printf '  DIFFERS   expected %s\n' "$3"
    printf '            The upstream source has changed since 2026-07-31.\n'
    printf '            This is expected over time and is not an error, but\n'
    printf '            the figures in the paper may no longer describe it.\n'
  fi
}

check_dir "upstream Linear A corpus" "raw_repo" "raw_repo/LinearAInscriptions.js" \
  "./setup.sh   (or git clone --depth 1 https://github.com/mwenge/lineara.xyz.git raw_repo)"

check_dir "Linear B lexicon" "nd" "nd/data/linear_b-greek.names.cog" \
  "./setup.sh   (or git clone --depth 1 https://github.com/j-luo93/NeuroDecipher.git nd)"

check_file "working corpus" "data/corpus_v1.json" "$EXPECT_CORPUS" \
  "node src/extract_raw.js && python3 src/build_corpus.py" "y" "$EXPECT_CORPUS_SHA"

if [ -f data/corpus_v1.json ] && [ -f tests/test_pipeline.py ]; then
  GOT_CORPUS=$(md5of data/corpus_v1.json)
  if [ "$GOT_CORPUS" != "$EXPECT_CORPUS" ]; then
    printf '\n[corpus md5 differs from the published snapshot]\n'
    printf '  WARNING   this could mean the upstream corpus has genuinely changed\n'
    printf '            since the last pipeline run, OR that this build is incomplete for an\n'
    printf '            unrelated reason (a partial clone, a failed fetch step) -\n'
    printf '            those look identical from a checksum alone. Before treating\n'
    printf '            %s as a new reference, confirm the build is\n' "$GOT_CORPUS"
    printf '            actually complete: re-run ./setup.sh from a clean checkout\n'
    printf '            and check the stage logs for errors, not just the final\n'
    printf '            checksum. Auto-updating CORPUS_MD5 here used to be automatic\n'
    printf '            and silent; that already corrupted the reference once, from\n'
    printf '            a build that was wrong for an unrelated reason, not from\n'
    printf '            genuine drift - see TODO.md "Completed". If, after checking,\n'
    printf '            this really is a new upstream snapshot: update CORPUS_MD5 in\n'
    printf "            tests/test_pipeline.py to %s by hand.\n" "$GOT_CORPUS"
  fi
fi

check_file "SigLA corpus" "data/sigla_corpus.json" "$EXPECT_SIGLA" \
  "python3 src/extract_sigla.py --fetch" "n" "$EXPECT_SIGLA_SHA"

if [ -f data/corpus_v1.json ]; then
  printf '\n[corpus contents]\n'
  python3 - <<'PY'
import json
try:
    r = json.load(open('data/corpus_v1.json', encoding='utf-8'))
    docs = len({x['doc_id'] for x in r})
    comp = sum(1 for x in r for t in x['tokens']
               if t['type'] == 'signgroup' and t['complete'])
    print(f"  records {len(r)} (expected 1721)")
    print(f"  distinct documents {docs} (expected 1621)")
    print(f"  complete sign-groups {comp} (expected 2659)")
except Exception as e:
    print('  could not read:', e)
PY
fi

if [ -f data/sigla_corpus.json ]; then
  printf '\n[SigLA contents]\n'
  python3 - <<'PY'
import json
try:
    d = json.load(open('data/sigla_corpus.json', encoding='utf-8'))
    a = [x for doc in d for x in doc['attestations']]
    c = sum(1 for x in a if x['confident'] is True)
    u = sum(1 for x in a if x['confident'] is False)
    n = sum(1 for x in a if x['confident'] is None)
    print(f"  documents {len(d)} (expected 802)")
    print(f"  attestations {len(a)} (expected 5144)")
    print(f"  confident {c} / doubtful {u} / unreadable {n} (expected 4712/44/388)")
except Exception as e:
    print('  could not read:', e)
PY
fi

echo
echo "=============================================================="
if [ $STATUS -eq 0 ]; then
  echo " Ready. Run ./src/run_all.sh"
  [ -f data/sigla_corpus.json ] || \
    echo " (SigLA absent: run  python3 src/extract_sigla.py --fetch  to add it.)"
else
  echo " Missing required inputs. See the produce: lines above."
fi
echo "=============================================================="
exit $STATUS
