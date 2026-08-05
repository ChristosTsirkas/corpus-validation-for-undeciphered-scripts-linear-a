#!/usr/bin/env bash
# Full pipeline, raw source -> all published figures. Deterministic.
# Stages must run in this order; later stages import earlier ones.
set -e
cd "$(dirname "$0")/.."   # run from repo root
echo "== S0  extract (drops translatedWords) ==";      node src/extract_raw.js
echo "== S1  build corpus ==";                         python3 src/build_corpus.py
echo "== S2  genre + structural ==";                   python3 src/structural.py
echo "== V1  parse Younger tabular ==";                python3 src/parse_younger.py
echo "== V2  sweep 1 (administrative) ==";             python3 src/sweep1.py
echo "== V3  parse Younger free-text ==";              python3 src/parse_younger_freetext.py
echo "== V4  sweep 2 (libation/non-tabular) ==";       python3 src/sweep2.py
echo "== A1  typology + affixation ==";                python3 src/typology.py
echo "== A2  affix null model ==";                     python3 src/affix_null.py
echo "== A3  grid feasibility ==";                     python3 src/grid_feasibility.py
echo "== A4  grid null model ==";                      python3 src/grid_null.py
echo "== A5  entropy + adequacy ==";                   python3 src/entropy.py
echo "== A6  phonological inheritance test ==";        python3 src/phonology_test.py
echo "== A7  power calibration ==";                    python3 src/power.py
echo "== A8  formula, dual reading ==";                python3 src/formula_dual.py
echo "== P1  Packard v4 (his rules, alternations) =="; python3 src/packard_v4.py
echo "== P2  Packard name parallels (Table 14) ==";    python3 src/packard_names.py
echo "== A9  KU-RO arithmetic ==";                     python3 src/kuro_test.py --fractions
echo "== V6  sweep 3 (SigLA, third witness) ==";       python3 src/sweep3.py
# A10 and A11 are SLOW (see docs/METHODOLOGY.md §6). Their published results are
# bundled at data/power_analysis.json. Set SLOW=1 to run them.
if [ "${SLOW:-0}" = "1" ]; then
  echo "== A10 sparse-data smoothing test ==";          python3 src/smoothing_test.py
  echo "== A11 affix-direction power (~20 min) ==";     python3 src/affix_power.py
else
  echo "== A10/A11 slow stages skipped (SLOW=1 to run) =="
fi
echo "== V5  final permutation validation ==";          python3 src/validate_final.py
echo "== done =="
