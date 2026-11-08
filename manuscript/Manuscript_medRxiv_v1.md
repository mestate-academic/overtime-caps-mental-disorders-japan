# Statutory overtime caps and compensated mental disorders in Japan: two natural experiments in 10 years of national data, 2016–2025

**Hironori Uematsu, MD, PhD, MPH¹**

¹ Uematsu Occupational Physician's Office (Mestate LLC), Kyoto, Japan

**Correspondence to:** Dr Hironori Uematsu, Uematsu Occupational Physician's Office, Nakagyo-ku, Kyoto, Japan; office@mestate.jp

**Preprint.** This manuscript has not been peer reviewed. It has been submitted to a journal. Version 1, November 2026.

**Licence:** CC BY 4.0. **Word count:** main text 3,727 words; abstract 291 words. **Tables:** 3. **Figures:** 2. **References:** 42. Supplementary material (4 tables, STROBE checklist) follows the main text.

**Keywords:** working hours; occupational stress; workers' compensation; mental disorders; health policy; difference-in-differences

---

## ABSTRACT

**Objectives** Japan capped overtime in two steps: most industries from April 2019 (large firms) or April 2020 (small and medium-sized firms), and construction and motor-vehicle driving, previously exempt, from April 2024. Within 10 years, this created two natural experiments. We examined whether either cap was followed by fewer compensated work-related mental disorders.

**Methods** Using national workers' compensation data for fiscal years (FY) 2016–2025 (April 2016–March 2026), we compared approvals and claims for mental disorders per million employed persons between construction and transport (exempt until 2024) and six comparison industries, using Poisson difference-in-differences and event-study models with small-cluster inference. Experiment 1 (April 2019/2020 cap) compared FY2016–2018 with FY2019–2023; experiment 2 (April 2024 cap) compared FY2021–2023 with FY2024–2025. Cerebro-cardiovascular disease, recognised mainly on the basis of long hours, served as a positive control for exposure: it should decline if the caps reduced extreme hours. We added sensitivity, placebo and prefecture-level analyses and grouped approvals by precipitating event.

**Results** Approvals more than doubled over the decade (498 to 1082). Neither cap was associated with a clear relative decline in the newly capped industries (experiment 1: incidence rate ratio [IRR] 1.07, wild cluster bootstrap 95% CI 0.77 to 1.50; experiment 2: 1.10, 0.93 to 1.50); both intervals included 1. Approvals in construction and transport rose sharply in FY2023, before enforcement, making experiment 2 sensitive to that year. Cerebro-cardiovascular approvals did not decline after either cap, but estimates were imprecise. Approvals classified under harassment rose from 21% to 50%, whereas working-hour events fell from 17% to 6%.

**Conclusions** In two natural experiments over 10 years, approvals for work-related mental disorders, counted by year of decision, were not lower in industries newly covered by statutory overtime caps. Because actual working hours, compliance and the timing of onset could not be measured, this does not show that reducing actual working hours is ineffective.

---

## KEY MESSAGES

**What is already known on this topic**
- Long working hours are associated with depression and suicide; Japan's overtime caps, in force from 2019, reduced paid overtime by about a quarter, but some men shifted to unpaid overtime.
- Whether statutory overtime caps reduce work-related mental disorders at population level is unknown.

**What this study adds**
- Japan's two-step introduction of overtime caps provided two natural experiments within 10 years of national data; in neither were compensated mental disorders lower after the cap.
- Cerebro-cardiovascular disease, the outcome most directly tied to long hours, also did not decline; the doubling of approvals was concentrated in cases classified under harassment, not working hours.

**How this study might affect research, practice or policy**
- Compensation statistics alone cannot show whether working-time policy works; monitoring should include measured hours, including unrecorded overtime.
- Prevention should also target harassment by supervisors and customers; these results should not be read as showing that the caps are unnecessary.

---

## INTRODUCTION

Long working hours are associated with depression, anxiety and suicide,¹⁻³ and the WHO/ILO Joint Estimates attributed 745 000 deaths from stroke and ischaemic heart disease in 2016 to working 55 hours or more per week.¹ Japan had no binding legal limit on overtime until the Work Style Reform Act of 2018.⁴ The Act capped overtime at 45 hours a month and 360 hours a year (up to 720 hours a year and 100 hours a month in exceptional cases), with penalties for violations. It applied to large firms from April 2019 and to small and medium-sized firms from April 2020; construction, motor-vehicle driving and physicians were exempt until April 2024 (the "2024 problem").⁵

The caps reduced long working hours, paid overtime by about 25%,⁶ ⁷ and, in a regression-discontinuity study, overtime above 45 and 80 hours a month among workers most likely to work long hours, although average effects were not robust;⁸ but some men replaced paid with unpaid overtime and gained no well-being.⁶ Earlier, a 2010 increase in the overtime wage premium reduced working hours and improved mental health,⁹ and the 2014 Act on overwork prevention, which set no limit on hours, was followed by an estimated 26% fall in compensated cerebro-cardiovascular disease across industries in a mediation analysis, about 41% of it through shorter working hours; mental disorders were not examined.¹⁰ Evaluations of the caps, including the government's own,¹¹ have measured working hours, wages and self-reported well-being; whether binding caps reduced work-related mental disorders is unknown. The workers' compensation system offers an annual measure: the Ministry of Health, Labour and Welfare (MHLW) publishes claims and approvals for mental disorders by industry, prefecture and precipitating event.¹² Approvals have risen every year since FY2018 and exceeded 1000 in FY2024,¹² and rates have long been highest in transport and postal services.¹³

The two-step introduction created two natural experiments within one decade (figure 1). From April 2019/2020, six industries were capped while construction and transport were not; from April 2024, construction and transport were capped while the six already were. Because compensation data also respond to the criteria for recognising mental disorders as work-related—revised in September 2023 to list customer harassment as a precipitating event¹⁴—and to claiming behaviour, we also analysed cerebro-cardiovascular disease, for which long working hours are the main recognition criterion, as a positive control for exposure: it should fall if the caps reduced extreme hours, and it shares the claiming environment of mental disorders. We asked whether either cap was followed by fewer compensated mental disorders in the newly capped industries.

## METHODS

### Design and data
We conducted a quasi-experimental study using publicly available aggregate data for the 10 fiscal years FY2016–2025 (April 2016 to March 2026), reported according to STROBE.¹⁵ From the MHLW annual reports¹²—each lists the current and the previous year, and the FY2025 report was published in July 2026—we transcribed, by industry, claims and approvals for mental disorders and for cerebro-cardiovascular diseases, and national approvals by precipitating event. Overlapping years were cross-checked, and approvals were also checked against a ministry compilation.¹⁶ Prefecture counts are published from FY2021. Counts refer to the fiscal year in which claims were filed or decided, not the year of onset, so some approvals after a cap concern illnesses that began before it. All transcribed tables summed to the published national totals (supplementary table S1). Denominators were annual average employed persons by industry from the Labour Force Survey¹⁷ and, for prefectures, the 2015 Population Census.¹⁸

### Two natural experiments
The exempt group comprised construction and transport and postal services (which includes motor-vehicle driving). Both groups also contain workers whose coverage did not change at the cap (for example, office staff in construction and non-driving occupations in transport), so the estimand is the association between an industry's legal coverage and its compensation rates, not the effect on individual covered workers. The comparison group comprised the six other industries reported separately throughout the period with consistent denominators: manufacturing; wholesale and retail; finance and insurance; education; information and communication; and accommodation and food services. Health care and welfare was capped in two steps—most workers from April 2019/2020 but physicians (about 4% of its workers) only from April 2024, with higher limits—so it fits neither group and is shown for reference only; the remaining divisions form a residual category and were not used. Because each cap took effect on 1 April, the first day of a fiscal year, every fiscal year lies wholly before or after each cap.

- **Experiment 1 (April 2019/2020 cap):** the six comparison industries were newly capped (large firms from April 2019, small and medium-sized firms from April 2020) and construction and transport served as controls; FY2016–2018 (before) was compared with FY2019–2023 (after), FY2019 being a transition year in which only large firms were capped.
- **Experiment 2 (April 2024 cap):** construction and transport were newly capped and the six industries served as controls; FY2021–2023 was compared with FY2024–2025.

The two experiments were estimated separately to avoid the problematic comparisons that arise from staggered treatment timing in a pooled model.¹⁹ Experiment 2 nevertheless used industries capped since April 2019/2020 as controls, so it estimates the change in construction and transport relative to industries already under a cap, not the effect against an uncapped counterfactual; any continuing change in the effect of the earlier cap among the controls would enter this estimate.

### Statistical analysis
We fitted Poisson regressions of annual counts with industry and year fixed effects, an interaction between the newly capped group and the post-cap period, log employed persons as offset, and heteroskedasticity-robust (HC1) standard errors, which also accommodate overdispersion. The primary outcome was approved claims for mental disorders; secondary outcomes were claims for mental disorders and approvals and claims for cerebro-cardiovascular diseases, which served as a positive control for exposure: long working hours are their main recognition criterion, and industry-average working hours predict compensated cases across industries,²⁰ so they should decline if the caps reduced extreme hours, whereas changes in claiming behaviour common to both diseases would move them together. For each experiment, an event study interacted the newly capped group with each year, relative to the mean (on the log scale) of that experiment's pre-cap period (FY2016–2018 or FY2021–2023), so that every year has an estimate and a CI; experiment 2's event study began in FY2020, the first year in which all six control industries were capped. Single reference years (FY2022, FY2023) were used in sensitivity analyses. The IRR from this model is the ratio of the after/before rate ratio in the newly capped group to that in the control group, so the control group's change stands in for what would have happened without the cap; this requires that, without the cap, the two groups would have followed parallel trends, which we examined with the pre-cap event-study estimates. 

Each experiment includes only eight industries (health care and welfare is shown for reference only), and HC1 standard errors do not account for serial correlation within industries. We therefore used a wild cluster score bootstrap, clustered by industry with Webb weights (9999 draws; 95% CIs by test inversion), as the primary method of inference for the main estimates.²¹⁻²³ Because only two industries were newly capped in experiment 2, and only two served as controls in experiment 1, even this bootstrap may be unreliable.²⁴ As sensitivity analyses, we also report standard errors clustered by industry with t(7) critical values, a placebo permutation analysis in which the model was re-estimated with each of the 28 pairs of the eight industries as placebo-treated, and estimates from the panel collapsed to one pre-cap and one post-cap period per industry.²⁵ Because the caps were not assigned at random, the permutation analysis is descriptive and its p values are not those of a randomization test. Prespecified sensitivity analyses excluded FY2023 (anticipation), FY2020–2021 (COVID-19) and accommodation and food services, extended experiment 2's pre-period to FY2016, and analysed construction and transport separately. To address the September 2023 addition of customer harassment, we also excluded wholesale and retail and accommodation and food services, the control industries most exposed to it. Post hoc analyses excluded the FY2019 transition year from experiment 1, added health care and welfare to the newly capped group in experiment 2, and used FY2019–2023 or FY2020–2023 as its pre-period. A prefecture panel (47 prefectures, FY2021–2025) related the 2015 share of employment in construction and transport (standardised) to approvals after 2024, with prefecture and year fixed effects and standard errors clustered by prefecture. Approvals by precipitating event were grouped into harassment, change in workload, working hours (≥80 hours of overtime in a month or ≥2 weeks of continuous work), accidents and injury, special events and other. Analyses used Python 3 and statsmodels 0.15; data and code are available at https://github.com/mestate-academic/overtime-caps-mental-disorders-japan.

### Patient and public involvement
Patients and the public were not involved.

### Ethics
Only publicly available aggregate statistics without information on identifiable individuals were used. Such research falls outside the scope of the Japanese Ethical Guidelines for Medical and Biological Research Involving Human Subjects,²⁶ and ethical review was not required.

## RESULTS

### Ten-year trends
Over the 10 years, approvals for mental disorders more than doubled, from 498 in FY2016 to 1082 in FY2025, and rose in every industry group (figure 1; table 1). The approval rate rose from 7.2 to 12.6 per million employed persons in the six comparison industries, from 11.9 to 24.5 in construction and transport, and from 9.9 to 30.8 in health care and welfare. Claims rose faster (24.0 to 64.2, 33.9 to 80.8 and 37.4 to 136.0 per million). Cerebro-cardiovascular approvals did not rise (table 1).

### Experiment 1: the April 2019/2020 cap
Approvals in the newly capped industries did not decline relative to construction and transport (IRR 1.07, 95% CI 0.92 to 1.24; table 2); with the wild cluster bootstrap the interval widened to 0.77 to 1.50. Claims rose (1.12, 1.02 to 1.23), but not significantly once clustering was accounted for (wild cluster bootstrap 0.82 to 1.53). Cerebro-cardiovascular approvals (1.01) and claims (0.96) did not change, but these estimates were imprecise (wild cluster bootstrap 0.40 to 1.57 and 0.75 to 1.18). In the event study (figure 2A), the pre-cap estimates for FY2016–2018 were close to 1 (0.94 to 1.04), consistent with parallel trends; approvals in the newly capped industries were not lower than before the cap in any year from FY2019 to FY2022 (IRRs 1.06 to 1.27); the IRR of 0.79 (0.68 to 0.92) in FY2023 reflects the rise in construction and transport that year. Cerebro-cardiovascular approvals did not change in any year (0.93 to 1.14).

### Experiment 2: the April 2024 cap
Approvals in construction and transport did not decline relative to the six comparison industries (IRR 1.10, 0.93 to 1.30; wild cluster bootstrap 0.93 to 1.50). Claims changed little (0.94, 0.87 to 1.03), nor did cerebro-cardiovascular approvals (0.96, 0.70 to 1.32) or claims (0.98, 0.88 to 1.08). In the event study (figure 2B), the relative rate in construction and transport was stable in FY2020–2022 (IRRs 0.87 to 0.99 relative to the FY2021–2023 mean), consistent with parallel trends until it rose in FY2023, the year before the cap (1.32, 1.20 to 1.46), and did not fall below the pre-cap level in FY2024 (1.08, 0.96 to 1.23) or FY2025 (1.18, 0.99 to 1.41) (supplementary table S2). The FY2023 rise preceded the cap and coincided with the September 2023 revision of the recognition criteria and intense media coverage of the "2024 problem"; it makes the parallel-trends assumption questionable for experiment 2, whose estimate depends on how that year is treated. With FY2022 as a single reference year, the IRRs were 1.53 (1.31 to 1.78) in FY2023, 1.25 (1.05 to 1.49) in FY2024 and 1.37 (1.14 to 1.64) in FY2025. Cerebro-cardiovascular approvals did not change in any year (0.85 to 1.07).

### Robustness
No method of inference indicated a decline in approvals in either experiment (supplementary table S3): the placebo permutation analysis gave p=0.68 and p=0.36, and the collapsed two-period estimates were 1.07 (0.94 to 1.21) and 1.10 (1.02 to 1.19). For some secondary outcomes, statistical significance depended on the method: for claims in experiment 2, the collapsed estimate was 0.95 (0.92 to 0.98), whereas the wild cluster bootstrap interval included 1 (0.85 to 1.21). Excluding FY2023, the IRRs were 1.19 (1.03 to 1.36) in experiment 1 and 1.30 (1.11 to 1.53) in experiment 2 (wild cluster bootstrap 0.90 to 1.62 and 1.07 to 2.00); because the FY2023 rise preceded the cap, these estimates show how strongly experiment 2 depends on the choice of reference period, not an increase caused by the cap. Other sensitivity analyses gave IRRs of 1.03 to 1.17 (supplementary table S3); excluding the FY2019 transition year, experiment 1 gave 1.03 (0.88 to 1.21); in experiment 2, adding health care and welfare to the newly capped group gave 1.13 (1.02 to 1.26), and using FY2019–2023 or FY2020–2023 as the pre-period gave 1.15 (1.00 to 1.33) and 1.11 (0.96 to 1.29). Excluding the two control industries most exposed to customer harassment gave 0.99 (0.85 to 1.17) and 1.10 (0.92 to 1.33). The experiment 2 estimate lay in the middle of the placebo distribution (0.79 to 1.15), which indicates no detectable effect rather than proof of no effect. In the prefecture panel, the exposure ranged from 9.7% (Tokyo) to 16.5% (Miyagi), and the IRR per SD was 1.03 (0.95 to 1.12) for approvals and 0.99 (0.96 to 1.01) for claims (supplementary table S4).

### Precipitating events
Over the decade, events classified as harassment rose from 21% to 50% of approvals, whereas working-hour events fell from 17% to 6% and did not increase in number (86 in FY2016, 70 in FY2025) (table 3). Of the 346 additional approvals between FY2022 and FY2024, 195 (56%) involved harassment—108 customer harassment, recognised from September 2023, and 77 power harassment by supervisors—and 28 (8%) working hours. Because harassment categories were added or redefined in May 2020 and September 2023, these shares are not fully comparable over time.

## DISCUSSION

### Principal findings
Japan's two-step introduction of overtime caps provided two natural experiments within 10 years of national data. In neither experiment were compensated mental disorders lower in the newly capped industries after the cap. Point estimates were at or above 1, and no method of inference indicated a decline, although intervals widened substantially once the small number of industries was taken into account. Recognition in construction and transport rose before the April 2024 cap, and the doubling of approvals was concentrated in cases classified under harassment rather than working hours, although changes in recognition criteria and claiming may have contributed. Cerebro-cardiovascular disease, the outcome most directly tied to long hours, did not decline after either cap.

### Were the caps complied with?
Our exposure was the legal cap, not the hours actually worked, and compliance was incomplete. In FY2024, inspectors visiting 26 512 workplaces suspected of long hours found illegal overtime in 42.4%; in these, the longest-working employee exceeded 80 hours of overtime in a month in 48.7% and 100 hours in 28.4%. Working time was inadequately recorded in 15.1%, and unpaid overtime was found in 8.0%.²⁷ In 2024, labour inspection offices handled 22 354 cases of unpaid wages affecting 185 197 workers.²⁸ These workplaces are not representative, but hours reported by households have long exceeded those reported by employers by about 300 hours per worker per year, a gap usually attributed to unpaid overtime,²⁹⁻³¹ and after the April 2019 cap some men replaced paid with unpaid overtime.⁶ Managers, workers under discretionary schemes and physicians (up to 1860 hours a year) were partly or wholly outside the caps. On the other hand, a regression-discontinuity study found that the 2019 cap reduced overtime above 45 and 80 hours a month among workers most likely to work long hours,⁸ so extreme hours may have fallen for some high-risk workers.

If the caps reduced recorded rather than actual hours—especially among the few workers with the longest hours, who generate most claims—the true change in exposure was much smaller than the legal change, and our estimates are biased towards the null. The positive control does not settle this question. Cerebro-cardiovascular approvals and claims did not fall after either cap, but the wild cluster bootstrap intervals for approvals (0.40 to 1.57 and 0.59 to 1.22) included substantial declines, and recognition of these diseases also depends on factors other than hours, including the recognition criteria, so their failure to decline is not evidence of non-compliance. Our findings therefore concern the legal caps, not the effect of reducing actual hours. Studies that make actual working time visible—for example, by estimating unrecorded overtime by industry from household and employer surveys, or by using electronic records of computer use and building entry—could overturn these findings and are needed.

### Other explanations
Three further mechanisms may contribute. First, working-hour events accounted for only 15–18% of approvals before the caps; most cases follow harassment, changes in workload or accidents, which the caps do not address. That hours-related approvals did not grow while total approvals doubled is compatible with a modest effect of the caps on such cases, but this nationwide effect cannot be identified here and was far smaller than the growth in other events. Second, regulation may raise awareness of compensation rights: claims rose in the newly capped industries after the April 2019/2020 cap, and approvals in construction and transport rose in FY2023, amid intense media coverage of the "2024 problem" but before the cap applied. Third, the September 2023 revision of recognition criteria raised approvals in all industries¹⁴ and may have affected them unequally; excluding the control industries most exposed to customer harassment did not change the results.

### Comparison with other studies
Earlier evaluations found fewer paid overtime hours with partial substitution by unpaid overtime⁶ and better self-rated health,⁷ declining long hours in construction and logistics before 2024,⁵ and a levelling-off of the decline in suicide among employed men around the time of the reform.³² We add that these changes have not, so far, reduced compensated mental disorders. Lin et al. reported a reduction in compensated cerebro-cardiovascular disease after the 2014 Act,¹⁰ whereas our difference-in-differences analyses found no clear additional relative reduction after the later caps. The findings are not directly comparable, because the studies evaluated different policies, periods and estimands: a nationwide before-after change in one, relative changes between industries in the other. Earlier improvements in working hours may have reduced the scope for further benefit, but our data did not capture the distribution of actual working hours. The predominance of interpersonal events agrees with analyses of Japanese compensation data³³ and with meta-analyses linking workplace bullying to depression.³⁴ ³⁵ Japan's harassment-prevention law, which required employers to prevent power harassment from June 2020 (large firms) and April 2022 (small and medium-sized firms), reduced self-reported harassment by about 7%,³⁶ but its effect on harassment-related disorders is unknown. Customer harassment has been listed as a specific precipitating event in the recognition criteria since September 2023, but employers were not required to prevent it until 1 October 2026, after our study period;³⁷ FY2027 will be the first full fiscal year in which compensation data can reflect that duty.

### Strengths and limitations
Strengths are complete national data over 10 years, two natural experiments in which the roles of the groups reverse, employment denominators, a positive control for exposure in both experiments, and prespecified sensitivity and placebo analyses. There are limitations. First, exposure was the legal cap, not measured hours. Second, the design is ecological with eight industries per experiment, of which only two were newly capped (experiment 2) or served as controls (experiment 1), so inference is imprecise and may remain unreliable even with the wild cluster bootstrap;²⁴ the exempt divisions include many workers who were never exempt, diluting exposure; and the April 2019/2020 cap reached small and medium-sized firms a year after large firms, which industry data cannot separate. Third, experiment 1 overlapped with the COVID-19 pandemic; excluding pandemic years or accommodation and food services did not change the results, but other industry-specific shocks cannot be excluded. Fourth, experiment 2 has only two post-cap years and controls that were already capped, so it estimates a relative change between industry groups rather than the absolute effect of the 2024 cap. Counts are by year of decision rather than onset, so approvals in FY2024–2025 include illnesses that began before April 2024; this may attenuate an immediate effect, although the direction and size of any bias are uncertain because filing and decision delays may have changed over time and differed between industries. Fifth, compensation data capture only claimed and recognised cases; the recognition criteria for mental disorders were revised in May 2020 and September 2023¹⁴ and those for cerebro-cardiovascular disease in September 2021,³⁸ all nationwide and therefore absorbed by year fixed effects unless their effect differed by industry; because earlier revisions in Japan and Taiwan, before our study period, were followed by more than twofold increases in recognised cerebro-cardiovascular cases,³⁹ ⁴⁰ a revision that affected industries unequally could bias our estimates. Sixth, prefecture-level exposure varied little (SD 1.3 percentage points). Seventh, denominators were all employed persons, including the self-employed, who are not covered by the compensation insurance and are numerous in construction; this understates rates and would bias the difference-in-differences estimates only if the self-employed share changed differently between the groups over the study period, which we could not examine. Denominators were not adjusted for age or sex.

### Implications
Preventing work-related mental disorders in Japan requires action on psychosocial hazards—above all harassment by supervisors and customers—alongside working-time regulation, and enforcement should target the recording of actual hours. Compensation statistics, whose annual records are widely reported, should not be used alone to judge working-time policy. This matters now: in October 2025, as the statutory five-year review of the Act began, the government instructed the ministry to consider relaxing working-time regulation,⁴¹ and from 1 September 2026 labour inspectors stopped uniformly requiring firms to reduce overtime to 45 hours a month, although the statutory caps are unchanged.⁴² Our results do not show that the caps are unnecessary: they concern compensation outcomes under incomplete compliance, not the health effects of reducing actual hours. Linking compensation records to measured hours, and extending follow-up beyond FY2025, would allow a more definitive evaluation.

## CONCLUSION
In national workers' compensation data, the introduction of Japan's statutory overtime caps was not associated with a clear relative reduction in approvals for work-related mental disorders in the industries studied, and the doubling of approvals was concentrated in cases classified under harassment. Industry-level differences in coverage, changes in recognition criteria, delayed decisions and the absence of measured working hours limit causal interpretation. These findings should not be read as evidence that reducing actual working hours is ineffective in preventing mental disorders.

---

**Contributors** HU conceived the study, collected and verified the data, performed the analyses and wrote the manuscript; HU is the sole author and guarantor.
**Funding** None.
**Competing interests** HU provides contracted occupational physician services to companies. No other interests.
**Data availability statement** Data are publicly available from the MHLW, the Statistics Bureau of Japan and e-Stat; transcribed datasets and code are available at https://github.com/mestate-academic/overtime-caps-mental-disorders-japan.

---

## REFERENCES (Vancouver)

1. Pega F, Náfrádi B, Momen NC, et al. Global, regional, and national burdens of ischemic heart disease and stroke attributable to exposure to long working hours for 194 countries, 2000–2016: a systematic analysis from the WHO/ILO Joint Estimates. *Environ Int* 2021;154:106595.
2. Rugulies R, Sørensen K, Di Tecco C, et al. The effect of exposure to long working hours on depression: a systematic review and meta-analysis from the WHO/ILO Joint Estimates. *Environ Int* 2021;155:106629.
3. Virtanen M, Jokela M, Madsen IE, et al. Long working hours and depressive symptoms: systematic review and meta-analysis of published studies and unpublished individual participant data. *Scand J Work Environ Health* 2018;44:239–50.
4. Act on the Arrangement of Related Acts to Promote Work Style Reform (Act No. 71 of 2018). Tokyo: MHLW, 2018.
5. Saito T. How much will working hours fall with the "2024 problem" in construction and logistics? Tokyo: NLI Research Institute, 2024 (in Japanese).
6. Burdin G, Kambayashi R, Kato T. The impact of overtime limits on firms and workers: evidence from Japan's Work Style Reform. IZA Discussion Paper No. 17583. Bonn: IZA, 2024 (revised 2026).
7. Kawaguchi D, Ogawa K. Can capping overtime improve worker welfare? Evidence from Japan's 2019 labor reform. RIETI Discussion Paper 26-E-034. Tokyo: RIETI, 2026.
8. Jiang M, Sasaki S. Do overtime regulations reduce overtime work in Japan? *J Jpn Int Econ* 2026;81:101436. doi:10.1016/j.jjie.2026.101436
9. Kohara M, Noda T. The causal effects of working time on mental health: the effectiveness of the law reform raising the overtime wage penalty. *Pac Econ Rev* 2023;28:638–64.
10. Lin RT, Liang YW, Takahashi M, et al. Effect of implementing an overwork-prevention act on working hours and overwork-related disease: a mediation analysis. *J Occup Health* 2020;62:e12148.
11. Ministry of Health, Labour and Welfare. Ex post evaluation of regulation: upper limits on overtime work (Labour Standards Act, article 36). Tokyo: MHLW, January 2025 (in Japanese).
12. Ministry of Health, Labour and Welfare. Status of workers' compensation for karoshi and related disorders, FY2016–FY2025. Tokyo: MHLW (annual; FY2025 edition published 15 July 2026; in Japanese).
13. Takahashi M. Sociomedical problems of overwork-related deaths and disorders in Japan. *J Occup Health* 2019;61:269–77.
14. Ministry of Health, Labour and Welfare. Recognition criteria for mental disorders caused by psychological burden: Notification Kihatsu 1226 No. 1, 26 December 2011, as revised by Notifications Kihatsu 0529 No. 1, 29 May 2020 (power harassment added) and Kihatsu 0901 No. 2, 1 September 2023 (customer harassment added). Tokyo: MHLW (in Japanese).
15. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *Lancet* 2007;370:1453–7.
16. Ministry of Health, Labour and Welfare, Labour Standards Bureau. Status of workers' compensation for mental disorders (committee material 2). Tokyo: MHLW, 2021 (in Japanese).
17. Statistics Bureau of Japan. Labour Force Survey, basic tabulation, table 2-5-1. e-Stat, 2026.
18. Statistics Bureau of Japan. 2015 Population Census, employment status basic tabulation, table 00510. e-Stat, 2017.
19. Goodman-Bacon A. Difference-in-differences with variation in treatment timing. *J Econom* 2021;225:254–77.
20. Lin RT, Chien LC, Kawachi I. Nonlinear associations between working hours and overwork-related cerebrovascular and cardiovascular diseases (CCVD). *Sci Rep* 2018;8:9694.
21. Cameron AC, Gelbach JB, Miller DL. Bootstrap-based improvements for inference with clustered errors. *Rev Econ Stat* 2008;90:414–27.
22. Kline P, Santos A. A score based approach to wild bootstrap inference. *J Econom Methods* 2012;1:23–41.
23. Webb MD. Reworking wild bootstrap-based inference for clustered errors. *Can J Econ* 2023;56:839–58.
24. MacKinnon JG, Webb MD. The wild bootstrap for few (treated) clusters. *Econom J* 2018;21:114–35.
25. Bertrand M, Duflo E, Mullainathan S. How much should we trust differences-in-differences estimates? *Q J Econ* 2004;119:249–75.
26. Ministry of Education, Culture, Sports, Science and Technology; Ministry of Health, Labour and Welfare; Ministry of Economy, Trade and Industry. Ethical Guidelines for Medical and Biological Research Involving Human Subjects. Tokyo, 2021 (partially revised 2023), Chapter 1, Section 3 (scope).
27. Ministry of Health, Labour and Welfare. Results of inspection and guidance at workplaces suspected of long working hours, FY2024. Tokyo: MHLW, 30 July 2025 (in Japanese).
28. Ministry of Health, Labour and Welfare. Results of inspection and guidance at workplaces suspected of wage non-payment, 2024. Tokyo: MHLW, 2025 (in Japanese).
29. Morioka K. Labour–management autonomy and legal regulation in the determination of working hours. *Japanese Journal of Labour Studies* 2016;58(677):53–63 (in Japanese).
30. Hoshino T. 195.8 hours of unpaid overtime per year: estimates from the Labour Force Survey and the Monthly Labour Survey. Economic Trends, 11 April 2017. Tokyo: Dai-ichi Life Research Institute, 2017 (in Japanese).
31. Sato K. Overtime work and its determinants: a comparative analysis of four panel datasets. RIETI Discussion Paper 19-J-006. Tokyo: RIETI, 2019 (in Japanese).
32. Matsumoto R, Motomura E, Okada M. Impacts of working hours, wages, and regular employment opportunity on suicide mortalities of employed and unemployed individuals before and during the COVID-19 pandemic in Japan. *Int J Environ Res Public Health* 2024;21:499.
33. Yamauchi T, Sasaki T, Yoshikawa T, et al. Differences in work-related adverse events by sex and industry in cases involving compensation for mental disorders and suicide in Japan from 2010 to 2014. *J Occup Environ Med* 2018;60:e178–82. doi:10.1097/JOM.0000000000001283
34. Theorell T, Hammarström A, Aronsson G, et al. A systematic review including meta-analysis of work environment and depressive symptoms. *BMC Public Health* 2015;15:738.
35. Verkuil B, Atasayi S, Molendijk ML. Workplace bullying and mental health: a meta-analysis on cross-sectional and longitudinal data. *PLoS One* 2015;10:e0135225.
36. Motegi H. Does harassment prevention law reduce harassment in workplaces? *Works Discussion Paper* 2021;55:1–16. Tokyo: Recruit Works Institute.
37. Act Partially Amending the Act on Comprehensive Promotion of Labour Policies and Other Acts (Act No. 63 of 2025, promulgated 11 June 2025; employer measures against customer harassment in force from 1 October 2026); Ministry of Health, Labour and Welfare Notification No. 51 of 26 February 2026 (guideline on employers' measures against customer harassment). Tokyo: MHLW (in Japanese).
38. Ministry of Health, Labour and Welfare. Recognition criteria for cerebrovascular and ischaemic heart disease caused by work: Notification Kihatsu 0914 No. 1, 14 September 2021. Tokyo: MHLW (in Japanese).
39. Lin RT, Lin CK, Christiani DC, et al. The impact of the introduction of new recognition criteria for overwork-related cardiovascular and cerebrovascular diseases: a cross-country comparison. *Sci Rep* 2017;7:167.
40. Lin SH, Chou MY, Lin RT. Mediation analysis for new recognition criteria, working hours and overwork-related disease: a nationwide ecological study using 11-year follow-up data in Taiwan. *BMJ Open* 2019;9:e028973.
41. Ministry of Health, Labour and Welfare. Press conference of the Minister of Health, Labour and Welfare on taking office, 22 October 2025 (instruction from the Prime Minister to consider relaxing working-time regulation, premised on health and worker choice). Tokyo: MHLW (in Japanese).
42. Ministry of Health, Labour and Welfare. Revision of consultation, support and inspection guidance on overtime work (press release, 19 August 2026; in force from 1 September 2026). Tokyo: MHLW (in Japanese).

---

## TABLES

**Table 1** Industries studied: employment and workers’ compensation in the three periods of the 10-year study

| Industry | Employed, million | MD claims, n P1 | MD claims, n P2 | MD claims, n P3 | MD approvals, n P1 | MD approvals, n P2 | MD approvals, n P3 | MD approval rate* P1 | MD approval rate* P2 | MD approval rate* P3 | CVD approvals, n P1 | CVD approvals, n P2 | CVD approvals, n P3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Construction & transport (exempt until April 2024)** | | | | | | | | | | | | | |
| Construction | 4.83 | 351 | 656 | 438 | 150 | 256 | 179 | 10.0 | 10.5 | 18.7 | 49 | 114 | 37 |
| Transport and postal services | 3.49 | 515 | 1116 | 699 | 158 | 344 | 214 | 15.5 | 19.7 | 31.0 | 290 | 316 | 152 |
| **Subtotal** | 8.32 | 866 | 1772 | 1137 | 308 | 600 | 393 | 12.3 | 14.3 | 23.9 | 339 | 430 | 189 |
| **Six comparison industries (capped from April 2019 or April 2020)** | | | | | | | | | | | | | |
| Manufacturing | 10.55 | 889 | 1921 | 1303 | 260 | 521 | 319 | 8.2 | 9.9 | 15.3 | 93 | 92 | 35 |
| Wholesale and retail | 10.41 | 708 | 1739 | 1190 | 190 | 416 | 236 | 5.9 | 7.9 | 11.4 | 88 | 147 | 57 |
| Finance and insurance | 1.55 | 177 | 352 | 182 | 29 | 60 | 33 | 5.9 | 7.3 | 10.6 | 2 | 3 | 1 |
| Education | 3.44 | 152 | 461 | 290 | 31 | 88 | 48 | 3.3 | 5.1 | 6.8 | 8 | 17 | 8 |
| Information and communication | 2.78 | 286 | 621 | 421 | 84 | 142 | 71 | 13.1 | 11.1 | 12.0 | 19 | 21 | 16 |
| Accommodation and food services | 3.98 | 246 | 596 | 416 | 93 | 217 | 139 | 7.8 | 11.1 | 16.9 | 80 | 87 | 47 |
| **Subtotal** | 32.71 | 2458 | 5690 | 3802 | 687 | 1444 | 846 | 7.1 | 8.8 | 12.8 | 290 | 367 | 164 |
| **Reference: physicians capped April 2024, other workers April 2019/2020** | | | | | | | | | | | | | |
| Health care and welfare | 9.1 | 935 | 3002 | 2271 | 232 | 751 | 562 | 9.4 | 17.0 | 30.1 | 18 | 43 | 22 |

Fiscal years (FY) run from April to March. Periods: P1, FY2016–2018 (April 2016–March 2019; before any cap); P2, FY2019–2023 (April 2019–March 2024; after the April 2019/2020 cap); P3, FY2024–2025 (April 2024–March 2026; after the April 2024 cap). MD, mental disorders; CVD, cerebro-cardiovascular diseases (positive control for exposure). *Approvals per million employed persons per year, using the mean employed persons of each period. Large firms were capped from April 2019 and small and medium-sized firms from April 2020. Employed persons: Labour Force Survey annual average, 2023.

**Table 2** Results of the two natural experiments (difference-in-differences)

| Outcome | IRR (95% CI)* | 95% CI, wild cluster bootstrap† | p† |
|---|---|---|---|
| **Experiment 1 (April 2019/2020 cap): six industries capped vs construction & transport; FY2016–18 vs FY2019–23** | | | |
| MD approvals | 1.07 (0.92 to 1.24) | 0.77 to 1.50 | 0.53 |
| MD approvals, excluding FY2023 | 1.19 (1.03 to 1.36) | 0.90 to 1.62 | 0.13 |
| MD claims | 1.12 (1.02 to 1.23) | 0.82 to 1.53 | 0.16 |
| CVD approvals (PC) | 1.01 (0.80 to 1.28) | 0.40 to 1.57 | 0.97 |
| CVD claims (PC) | 0.96 (0.85 to 1.08) | 0.75 to 1.18 | 0.68 |
| **Experiment 2 (April 2024 cap): construction & transport capped vs six industries; FY2021–23 vs FY2024–25** | | | |
| MD approvals | 1.10 (0.93 to 1.30) | 0.93 to 1.50 | 0.16 |
| MD approvals, excluding FY2023 | 1.30 (1.11 to 1.53) | 1.07 to 2.00 | 0.03 |
| MD claims | 0.94 (0.87 to 1.03) | 0.85 to 1.21 | 0.17 |
| CVD approvals (PC) | 0.96 (0.70 to 1.32) | 0.59 to 1.22 | 0.76 |
| CVD claims (PC) | 0.98 (0.88 to 1.08) | 0.86 to 1.10 | 0.61 |
| **Experiment 2, prefecture panel: per SD of exposure; FY2021–23 vs FY2024–25** | | | |
| MD approvals | 1.03 (0.95 to 1.12) | – | 0.48‡ |
| MD claims | 0.99 (0.96 to 1.01) | – | 0.30‡ |

IRR, ratio of the after/before rate ratio in the newly capped group to that in the control group (difference-in-differences); IRR<1 would indicate a decline in the newly capped group relative to what the control group's change implies. Fiscal years (FY) run from April to March. MD, mental disorders; CVD, cerebro-cardiovascular diseases; PC, positive control for exposure (should decline if the caps reduced extreme hours). Poisson regression with unit and year fixed effects and log employed persons as offset. *95% CI from heteroskedasticity-robust (HC1) standard errors. †Wild cluster score bootstrap clustered by industry (eight clusters; Webb weights, 9999 draws; CI by test inversion), the primary method of inference; it allows for serial correlation but may be unreliable with only two newly capped (experiment 2) or control (experiment 1) industries. ‡Prefecture models: standard errors clustered by prefecture (47 clusters). Exposure: standardised 2015 share of employment in construction and transport. Clustered, placebo-permutation and collapsed two-period estimates and sensitivity analyses in supplementary table S3.

**Table 3** Approved claims for mental disorders by precipitating event, FY2016–2025

| Event group | Approved claims, n '16 | Approved claims, n '17 | Approved claims, n '18 | Approved claims, n '19 | Approved claims, n '20 | Approved claims, n '21 | Approved claims, n '22 | Approved claims, n '23 | Approved claims, n '24 | Approved claims, n '25 | Share, % 2016 | Share, % 2025 | Δ 22–24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Harassment | 103 | 123 | 102 | 121 | 214 | 246 | 286 | 371 | 481 | 538 | 21 | 50 | +195 |
|  Power harassment† | – | – | – | – | 99 | 125 | 147 | 157 | 224 | 222 | – | – | +77 |
|  Bullying/violence‡ | 74 | 88 | 69 | 79 | 71 | 61 | 73 | 59 | 44 | 62 | – | – | -29 |
|  Sexual harassment | 29 | 35 | 33 | 42 | 44 | 60 | 66 | 103 | 105 | 127 | – | – | +39 |
|  Customer harassment§ | – | – | – | – | – | – | – | 52 | 108 | 127 | – | – | +108 |
| Workload change | 63 | 64 | 69 | 68 | 58 | 71 | 78 | 100 | 120 | 113 | 13 | 10 | +42 |
| Working hours¶ | 86 | 89 | 70 | 74 | 72 | 67 | 59 | 68 | 87 | 70 | 17 | 6 | +28 |
| Accidents/injury | 95 | 89 | 92 | 83 | 133 | 98 | 131 | 158 | 135 | 153 | 19 | 14 | +4 |
| Special events | 67 | 63 | 55 | 63 | 54 | 63 | 61 | 71 | 78 | 74 | 13 | 7 | +17 |
| Other | 84 | 78 | 77 | 100 | 77 | 84 | 95 | 115 | 155 | 134 | 17 | 12 | +60 |
| **Total** | 498 | 506 | 465 | 509 | 608 | 629 | 710 | 883 | 1056 | 1082 | 100 | 100 | +346 |

FY, fiscal year, April to March (’16 = FY2016, April 2016–March 2017). Δ 22–24, change in approved claims between FY2022, the last fiscal year decided wholly under the May 2020 criteria, and FY2024, the first decided wholly under the September 2023 criteria (total +346); this interval contains the largest two-year increase of the decade. †Recognised as a separate event from May 2020; before then included under bullying/violence or conflict with supervisors. ‡Before May 2020, “severe harassment, bullying or violence” (including by supervisors). §Listed as a precipitating event in the compensation criteria from September 2023; an employer duty to prevent customer harassment took effect on 1 October 2026, after the study period. ¶≥80 hours of overtime in a month or ≥2 weeks of continuous work. FY2016–2019 follow the 2011 recognition criteria; categories are not fully comparable across the May 2020 and September 2023 revisions.

## FIGURE LEGENDS

**Figure 1** Ten-year trends in workers' compensation for mental disorders, FY2016–2025. (A) Approved claims and (B) claims filed per million employed persons. Each point is one fiscal year (April to March), plotted at that year's label. Because each cap took effect on 1 April, the first day of a fiscal year, the boundaries of the shaded bands mark the caps. Shading shows the three periods that define the two natural experiments: no cap (FY2016–2018); six comparison industries capped (large firms from April 2019, small and medium-sized firms from April 2020, dotted line; FY2019–2023); all industries capped, including construction and transport (from April 2024; FY2024–2025). Six comparison industries: manufacturing; wholesale and retail; finance and insurance; education; information and communication; accommodation and food services. Health care and welfare (dashed) is shown for reference: physicians were capped from April 2024 and other workers from April 2019/2020. Denominators: Labour Force Survey.

**Figure 2** Event studies for the two natural experiments. (A) Experiment 1 (April 2019/2020 cap): six comparison industries (newly capped) vs construction and transport (control), FY2016–2023, relative to the mean of FY2016–2018. (B) Experiment 2 (April 2024 cap): construction and transport (newly capped) vs six comparison industries (control), FY2020–2025, relative to the mean of FY2021–2023. Every point, including those in the reference period, uses the same reference: it is the incidence rate ratio (IRR), with 95% CI, of the rate in the newly capped group relative to the control group in that year, divided by the mean of this ratio over the reference period (geometric mean, set to 1). Filled circles, approved claims for mental disorders (main outcome); open squares, cerebro-cardiovascular disease (positive control for exposure). An IRR below 1 indicates a decline in the newly capped group relative to its pre-cap level. Poisson regression with industry and year fixed effects, log employed persons as offset and robust (HC1) standard errors, which do not account for the small number of industries, so the intervals may be too narrow (see supplementary table S3). Shading as in figure 1.

**Supplementary material:** table S1 (transcription checks against national totals), table S2 (event studies for both experiments, relative to the pre-cap mean), table S3 (sensitivity analyses and small-cluster inference), table S4 (prefecture panel models), STROBE checklist.
