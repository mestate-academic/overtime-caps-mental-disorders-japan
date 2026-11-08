#!/usr/bin/env bash
# Reproduce all datasets, tables and figures. Run from the repository root.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p output/intermediate output/tables output/figures manuscript
echo "1/7 building data"; for s in build_data build_data2 build_data3 build_data4 build_data5; do python3 code/$s.py >/dev/null; done
echo "2/7 industry rates and basic models";   python3 code/analyze2.py >/dev/null
echo "3/7 prefecture panel";                   python3 code/analyze3.py >/dev/null
echo "4/7 precipitating events";               python3 code/analyze4.py >/dev/null; python3 code/build_events_2016.py >/dev/null
echo "5/7 main DiD, sensitivity, placebo, Table 1"; python3 code/analyze5_sensitivity.py >/dev/null
echo "6/7 event studies";                      python3 code/analyze6_eventstudy_pooled.py >/dev/null
echo "6b/7 small-cluster inference (about 2 minutes)"; python3 code/analyze7_inference.py >/dev/null 2>&1
echo "7/7 figures and tables S1-S4";           python3 code/make_figs_en.py >/dev/null
echo "done: output/tables, output/figures"
if command -v node >/dev/null && [ "${BUILD_DOCX:-0}" = 1 ]; then
  echo "building Word manuscript"; python3 code/build_spec.py >/dev/null; node code/render_docx.js
fi
