# Statutory overtime caps and compensated mental disorders in Japan: two natural experiments in 10 years of national data, 2016–2025

Data and code for the manuscript by Hironori Uematsu (Uematsu Occupational Physician's Office / Mestate LLC, Kyoto, Japan). Correspondence: office@mestate.jp.

Repository: https://github.com/mestate-academic/overtime-caps-mental-disorders-japan

Preprint: medRxiv [DOI to be added]. Journal: submitted to *Occupational and Environmental Medicine*.

## What is here

| Folder | Contents |
|---|---|
| `data/` | Transcribed public statistics (CSV, UTF-8). See `data/DATA_DICTIONARY.md` for every file, column and source. |
| `code/` | Python scripts that build the datasets, run the analyses and draw the figures, plus the scripts that assemble the Word manuscript. |
| `output/tables/` | Table 1 and supplementary tables S1–S8 as produced by the code. |
| `output/figures/` | Figures 1, 2, S1, S2 (PNG, 300 dpi). |
| `output/intermediate/` | Intermediate CSVs written by the analysis scripts (created when the code is run). |
| `manuscript/` | Manuscript text (Markdown, English and Japanese) and the rendered Word files. |

All data are aggregate statistics published by the Japanese government; no individual-level data are included.

## Reproducing the results

Requirements: Python ≥3.11 with the packages in `requirements.txt` (tested with Python 3.13, pandas 3.0.5, numpy 2.5.3, statsmodels 0.15.0, matplotlib 3.11.2, Pillow 12.3.0). Node.js ≥20 with the `docx` package (tested 9.8.1) is needed only for `render_docx.js`.

Run everything from the repository root:

```bash
pip install -r requirements.txt
bash run_all.sh
```

`run_all.sh` runs the steps below in order. Each step can also be run on its own.

| Step | Script | Produces |
|---|---|---|
| 1 Build data | `code/build_data.py`, `build_data2.py`, `build_data3.py`, `build_data4.py`, `build_data5.py` | the CSVs in `data/` (the committed CSVs are identical to the output of these scripts) |
| 2 Rates and basic DiD | `code/analyze2.py` | `output/intermediate/t6_industry_rates.csv` (industry × year panel with employment denominators), `t7_group_rates.csv`, `t8`, `t9` |
| 3 Prefecture panel | `code/analyze3.py` | `t12_pref_panel.csv`, `t13`, `t14_pref_did.csv` |
| 4 Precipitating events | `code/analyze4.py`, `code/build_events_2016.py` | `t17_events_approvals.csv`, `t24_events_2016_2025.csv` (Table 3) |
| 5 Main DiD, sensitivity, placebo, Table 1 | `code/analyze5_sensitivity.py` | `output/tables/Table1_descriptive.csv`, `TableS6`, `TableS7_sensitivity.csv`, `TableS8`, `placebo.txt` |
| 6 Event studies | `code/analyze6_eventstudy_pooled.py` | `TableS5_eventstudy_pooled.csv`, `t25_es_pooled.csv` (Figure 2) |
| 6b Small-cluster inference | `code/analyze7_inference.py` | `TableS3b_inference.csv` (industry-clustered SEs, wild cluster score bootstrap with Webb weights, randomization inference, collapsed two-period models; supplementary table S3 and the wild-bootstrap column of Table 2), `inference_summary.pkl`; seed 20261108 |
| 7 Figures and tables S1–S4 | `code/make_figs_en.py` | `output/figures/*.png`, `TableS1–S4` |
| 8 Word manuscript (optional) | `code/build_spec.py`, `node code/render_docx.js` | `manuscript/Manuscript_OEM_v8.docx`, `Supplementary_OEM_v6.docx` |

The main estimates in Table 2 of the paper (experiment 1: IRR 1.07, robust 95% CI 0.92 to 1.24, wild cluster bootstrap 0.77 to 1.50; experiment 2: IRR 1.10, 0.93 to 1.30 and 0.93 to 1.50) are in `output/tables/TableS7_sensitivity.csv` ("Main") and `output/tables/TableS3b_inference.csv`.

## Analysis in brief

- **Design.** Two natural experiments created by Japan's two-step overtime caps (Work Style Reform Act, Act No. 71 of 2018): experiment 1, six industries capped from April 2019 (large firms) / April 2020 (small and medium-sized firms) vs construction and transport (exempt), FY2016–2018 vs FY2019–2023; experiment 2, construction and transport capped from April 2024 vs the six industries, FY2021–2023 vs FY2024–2025.
- **Model.** Poisson regression of annual counts with industry and fiscal-year fixed effects, an interaction between the newly capped group and the post-cap period, log employed persons as offset, HC1 standard errors; with eight industries per experiment, inference is also reported with industry-clustered SEs, a wild cluster score bootstrap, randomization inference and collapsed two-period models. The IRR is the ratio of the after/before rate ratio in the newly capped group to that in the control group. Event studies are referenced to the log-scale mean of each experiment's pre-cap period.
- **Outcomes.** Approved claims (primary) and claims for work-related mental disorders; approvals and claims for cerebro-cardiovascular disease as a positive control for exposure.
- **Additional analyses.** Permutation (placebo) test over all 28 pairs of the eight industries; prefecture panel (47 prefectures, FY2021–2025) using the 2015 share of employment in construction and transport as exposure intensity; approvals by precipitating event.

Fiscal years (FY) run from April to March; FY2025 = April 2025–March 2026.

## Sources of the data

All sources are Japanese government publications; details per file are in `data/DATA_DICTIONARY.md`.

- Ministry of Health, Labour and Welfare (MHLW), 過労死等の労災補償状況 (Status of workers' compensation for karoshi and related disorders), annual, FY2016–FY2025 editions (FY2025 edition published 15 July 2026). Tables 1-2, 2-2, 2-5, 2-8 of the annex.
- MHLW Labour Standards Bureau, 精神障害の労災補償状況 (committee material 2, 2021), used to cross-check approvals.
- Statistics Bureau of Japan, Labour Force Survey, basic tabulation, table 2-5-1 (employed persons by industry, annual averages).
- Statistics Bureau of Japan, 2015 Population Census, employment status basic tabulation, table 00510 (employed persons by industry and prefecture).
- Files not used in the paper but kept for completeness (patient survey, suicide statistics, population by age) are marked as such in the data dictionary.

## Licence

Code: MIT License (see `LICENSE`). Transcribed data (`data/`) and outputs: CC BY 4.0; the underlying statistics are published by the Government of Japan under its Standard Terms of Use (compatible with CC BY 4.0) and should be credited to the issuing ministry.

## Citation

See `CITATION.cff`. Please cite the paper once published; until then, cite the medRxiv preprint and this repository (Zenodo DOI to be added).

---

## 日本語の概要

本リポジトリは、論文「時間外労働の上限規制と精神障害の労災補償：10年間の全国データにおける2つの自然実験（2016–2025年度）」のデータとコードです。

- `data/`：厚生労働省「過労死等の労災補償状況」（各年度）、労働力調査、平成27年国勢調査から転記した集計統計（CSV）。個人データは含みません。各ファイルの列と出典は `data/DATA_DICTIONARY.md` を参照。
- `code/`：データ構築（`build_data*.py`）、解析（`analyze2`〜`analyze6`、`build_events_2016.py`）、図（`make_figs_en.py`）、Word原稿の生成（`build_spec.py`、`render_docx.js`）。
- `output/`：論文の表1・補足表S1〜S8と図1・2・S1・S2。
- `manuscript/`：原稿（英語・日本語訳）。

再現は、リポジトリのルートで `pip install -r requirements.txt` の後に `bash run_all.sh` を実行してください。主要推定値（実験1 IRR 1.07、実験2 IRR 1.10）は `output/tables/TableS7_sensitivity.csv` の "Main" 行に出力されます。
