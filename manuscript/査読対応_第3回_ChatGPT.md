# 査読への対応（第3回：ChatGPT）

判定：ChatGPT＝**Minor Revision**（第2回のMajor Revisionから改善。「OEMへの投稿を進めてよい水準」）。`run_all.sh` を独立に実行し、雇用者数分母を含む主要結果と、雇用者数の転記値（労働力調査2025年平均・表Ⅰ－８）が一致することを確認済み。

主要な数値・解析は変更なし。表記と補足表の整理のみ。本文3,165語、抄録246語、文献40件、図表5点。

---

## Major

| # | 指摘 | 対応 |
|---|---|---|
| 1 | 補足表S3bのプラセボ並べ替え分析の「95% CI」（実験1 0.58〜1.50、実験2 0.69〜1.23）は、割付が無作為でも交換可能でもないため信頼区間として示すべきでない。p値も記述的な順位指標と脚注で明記 | **採用。** S3bの並べ替えの行は区間を削除し「IRR（no interval）」とし、方法名を「Placebo permutation (28 assignments; descriptive)」に変更。脚注に「並べ替えの結果は記述的なものに限る。p値は28通りのプラセボ推定値の中での観察値の順位であり、p値も検定の反転による区間も、割付が無作為・交換可能でないためランダム化に基づく推論と解釈すべきでない。したがって区間は示さない」と明記。本文の頑健性の記述も「descriptive placebo permutation p values」とした |
| 2 | 少数クラスターの制約は引き続き明示。S3aの列見出しを「IRR (95% CI, HC1)」に | **採用。** S3aの列見出しを変更し、脚注に「HC1は業種数の少なさを考慮しない（少数クラスター推論はS3b）」と追記。方法・限界・S3bの制約の記述は維持 |

## Minor

| # | 指摘 | 対応 |
|---|---|---|
| 1 | Key messagesは規定で3〜5文。現在6文 | **採用。** 「既に分かっていること」を1文にまとめ、計5文に |
| 2 | READMEに旧名称「randomization inference」が残る。レビュー用zipにないbuild_spec.py・render_docx.jsに言及。DATA_DICTIONARYの見出し順の混在 | **採用。** READMEを「placebo permutation analysis」に統一し、Word生成用の2ファイルは査読用パッケージに含めない旨を注記。DATA_DICTIONARYは国勢調査の節の後に雇用者数の節を独立した見出しで配置 |
| 3 | 「最も長時間働く少数の労働者が請求の大半を生む」は本研究で未検証。帰無方向への偏りを断定しない | **採用。** 推奨文のとおり「If the caps reduced recorded rather than actual working hours, the change in relevant exposure may have been smaller than the legal change, potentially attenuating any observable effect on compensation outcomes.」に差し替え |
| 4 | 文献の追加・削除は適切。約300時間は推定方法で変わる。文献29の英語タイトルをRIETIの公式表記に | **採用。** 「推定方法により年数百時間」と表現を変更。文献29を「Actual condition of overtime and its determinants: comparative analysis using four panel data sets」に修正 |
| 5 | Key messagesの「lower after the cap」は区間の広さが伝わりにくい。結論と表現を統一 | **採用。** 「neither overtime cap was associated with a clearly detectable relative reduction in compensated work-related mental disorders」に変更 |

## 投稿準備

- OEMには本文をWord（Manuscript_OEM_v8.docx）、図2点を別ファイル（Figure1.png、Figure2.png）、補足資料（Supplementary_OEM_v6.pdf／.docx）、STROBEチェックリスト（STROBE_checklist_OEM）、カバーレターで提出する。投稿パッケージに同梱済み。
- リポジトリで `bash run_all.sh` を再実行し、全表の数値が変わらないことを確認。
