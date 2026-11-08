# -*- coding: utf-8 -*-
"""Parse Manuscript_OEM_v3.md + supplementary CSVs into JSON specs for docx rendering."""
import re, json, pandas as pd
O='output/intermediate/'; S='output/tables/'

def runs(text):
    out=[]
    for tok in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)',text):
        if not tok: continue
        if tok.startswith('**'): out.append([tok[2:-2],1,0])
        elif tok.startswith('*'): out.append([tok[1:-1],0,1])
        else: out.append([tok,0,0])
    return out

def widths(header,rows,total=9026,minw=900,first=None):
    L=[max([len(str(header[j]))*0.8]+[len(str(r[j])) for r in rows]) for j in range(len(header))]
    L=[max(l,6) for l in L]
    if first: L[0]=max(L[0],first)
    w=[total*l/sum(L) for l in L]
    for _ in range(20):
        small=[i for i,x in enumerate(w) if x<minw]
        if not small: break
        deficit=sum(minw-w[i] for i in small); big=[i for i in range(len(w)) if i not in small]
        for i in small: w[i]=minw
        tb=sum(w[i] for i in big)
        for i in big: w[i]-=deficit*w[i]/tb
    w=[int(x) for x in w]; w[0]+=total-sum(w); return w

def parse_table(lines):
    rows=[[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if not re.match(r'^\|[-| ]+\|$',l.strip())]
    return rows[0],rows[1:]

import sys
VER=sys.argv[1] if len(sys.argv)>1 else 'v8'
md=open(f'manuscript/Manuscript_OEM_{VER}.md').read()
body,rest=md.split('## TABLES')
tabsec,legsec=rest.split('## FIGURE LEGENDS')

blocks=[]
for para in body.split('\n'):
    l=para.rstrip()
    if not l: continue
    if l=='---': blocks.append({'t':'pb'}); continue
    m=re.match(r'^(#+) (.*)',l)
    if m:
        lvl=len(m.group(1)); txt=m.group(2)
        if txt.startswith('REFERENCES'): blocks.append({'t':'pb'}); txt='REFERENCES'
        blocks.append({'t':'h%d'%lvl,'text':txt}); continue
    if l.startswith('- '): blocks.append({'t':'bullet','runs':runs(l[2:])}); continue
    m=re.match(r'^(\d+)\. (.*)',l)
    if m: blocks.append({'t':'ref','n':m.group(1),'runs':runs(m.group(2))}); continue
    blocks.append({'t':'p','runs':runs(l)})
# drop page-break duplicates
clean=[]
for b in blocks:
    if b['t']=='pb' and clean and clean[-1]['t']=='pb': continue
    clean.append(b)
blocks=clean

# tables
chunks=re.split(r'\n(?=\*\*Table \d)',tabsec.strip())
tables=[]
for c in chunks:
    ls=c.strip().split('\n'); title=ls[0]
    tl=[l for l in ls if l.startswith('|')]; notes=[l for l in ls[1:] if l.strip() and not l.startswith('|')]
    h,r=parse_table(tl)
    tables.append({'title':runs(title),'header':h,'rows':r,'widths':widths(h,r),'note':' '.join(notes)})
for t in tables:
    if 'precipitating' in str(t['title']):
        t['widths']=[2726,900,900,900,900,900,1800]
        t['note']='Percentages in the year columns are of all approvals in that year; percentages in the last column are of the total change between FY2022 and FY2024 (+346). Customer harassment was added to the recognised events in September 2023. Sub-items of harassment are not exhaustive (bullying or violence by co-workers not shown).'
    if 'Difference' in str(t['title']):
        t['widths']=[2000,2500,2000,1726,800]
        t['note']='IRR, incidence rate ratio. Industry-level models include industry and year fixed effects, log employed persons as offset and heteroskedasticity-robust (HC1) standard errors. Prefecture models include prefecture and year fixed effects and standard errors clustered by prefecture; exposure is the standardised 2015 share of employment in construction and transport.'
    if 'Characteristics of the industries' in str(t['title']):
        t['widths']=[1900,420]+[820]*13; t['font']=16; t['landscape']=True


# ---------- compact main tables (built from data, replace parsed markdown tables) ----------
T1=pd.read_csv(S+'Table1_descriptive.csv'); E1=open(S+'T1_total_Exe.csv').read().split('\n')[1].split(','); N1=open(S+'T1_total_Non.csv').read().split('\n')[1].split(',')
def t1row(name,v):  # v: [emp, cl1,cl2,cl3, ap1,ap2,ap3, cvd1,cvd2,cvd3, r1,r2,r3]
    v=[str(x) for x in v]; return [name,v[0]]+v[1:4]+v[4:7]+v[10:13]+v[7:10]
rows1=['§Construction & transport (exempt until April 2024)']
for i in [0,1]: rows1.append(t1row(T1.iloc[i,0],T1.iloc[i,2:].tolist()))
rows1.append(t1row('**Subtotal**',E1[2:]))
rows1.append('§Six comparison industries (capped from April 2019 or April 2020)')
for i in range(2,8): rows1.append(t1row(T1.iloc[i,0],T1.iloc[i,2:].tolist()))
rows1.append(t1row('**Subtotal**',N1[2:]))
rows1.append('§Reference: physicians capped April 2024, other workers April 2019/2020')
rows1.append(t1row(T1.iloc[8,0],T1.iloc[8,2:].tolist()))
P3=['P1','P2','P3']
tab1={'title':[['Table 1',1,0],[' Industries studied: employment and workers\u2019 compensation in the three periods of the 10-year study',0,0]],
 'groups':[['',1],['',1],['MD claims, n',3],['MD approvals, n',3],['MD approval rate*',3],['CVD approvals, n',3]],
 'header':['Industry','Employed, million']+P3*4,'rows':rows1,'widths':[1922,900]+[517]*12,'font':15,
 'note':'Fiscal years (FY) run from April to March. Periods: P1, FY2016–2018 (April 2016–March 2019; before any cap); P2, FY2019–2023 (April 2019–March 2024; after the April 2019/2020 cap); P3, FY2024–2025 (April 2024–March 2026; after the April 2024 cap). MD, mental disorders; CVD, cerebro-cardiovascular diseases (positive control for exposure). *Approvals per million employed persons per year, using the mean employed persons of each period. Large firms were capped from April 2019 and small and medium-sized firms from April 2020. Employed persons: Labour Force Survey annual average, 2023.'}
_sm=pd.read_pickle(O+'inference_summary.pkl')
def _w(k):
    v=_sm[k]['wild']; return f'{v[0]:.2f} to {v[1]:.2f}'
def _p(k):
    p=_sm[k].get('pw',_sm[k].get('p')); return '<0.001' if p<0.001 else (f'{p:.3f}' if p<0.01 else f'{p:.2f}')
rows2=['§Experiment 1 (April 2019/2020 cap):\nSix industries capped vs construction & transport; FY2016–18 vs FY2019–23',
 ['MD approvals','1.07 (0.92 to 1.24)',_w((1,'approvals')),_p((1,'approvals'))],['MD approvals, excluding FY2023','1.19 (1.03 to 1.36)',_w((1,'approvals_x23')),_p((1,'approvals_x23'))],['MD claims','1.12 (1.02 to 1.23)',_w((1,'claims')),_p((1,'claims'))],['CVD approvals (PC)','1.01 (0.80 to 1.28)',_w((1,'cvd_approvals')),_p((1,'cvd_approvals'))],['CVD claims (PC)','0.96 (0.85 to 1.08)',_w((1,'cvd_claims')),_p((1,'cvd_claims'))],
 '§Experiment 2 (April 2024 cap):\nConstruction & transport capped vs six industries; FY2021–23 vs FY2024–25',
 ['MD approvals','1.10 (0.93 to 1.30)',_w((2,'approvals')),_p((2,'approvals'))],['MD approvals, excluding FY2023','1.30 (1.11 to 1.53)',_w((2,'approvals_x23')),_p((2,'approvals_x23'))],['MD claims','0.94 (0.87 to 1.03)',_w((2,'claims')),_p((2,'claims'))],['CVD approvals (PC)','0.96 (0.70 to 1.32)',_w((2,'cvd_approvals')),_p((2,'cvd_approvals'))],['CVD claims (PC)','0.98 (0.88 to 1.08)',_w((2,'cvd_claims')),_p((2,'cvd_claims'))],
 '§Experiment 2, prefecture panel:\nPer SD of exposure; FY2021–23 vs FY2024–25',
 ['MD approvals','1.03 (0.95 to 1.12)','–','0.48‡'],['MD claims','0.99 (0.96 to 1.01)','–','0.30‡']]
tab2={'title':[['Table 2',1,0],[' Results of the two natural experiments (difference-in-differences)',0,0]],'header':['Outcome','IRR (95% CI)*','95% CI, wild cluster bootstrap†','p†'],'rows':rows2,'widths':[3326,2500,2200,1000],'font':18,
 'note':'IRR, ratio of the after/before rate ratio in the newly capped group to that in the control group (difference-in-differences); IRR<1 would indicate a decline in the newly capped group relative to what the control group\u2019s change implies. Fiscal years (FY) run from April to March. MD, mental disorders; CVD, cerebro-cardiovascular diseases; PC, positive control for exposure (should decline if the caps reduced extreme hours). Poisson regression with unit and year fixed effects and log employed persons as offset. *95% CI from heteroskedasticity-robust (HC1) standard errors. \u2020Wild cluster score bootstrap clustered by industry (eight clusters; Webb weights, 9999 draws; CI by test inversion), the primary method of inference; it allows for serial correlation but may be unreliable with only two newly capped (experiment 2) or control (experiment 1) industries. \u2021Prefecture models: standard errors clustered by prefecture (47 clusters). Exposure: standardised 2015 share of employment in construction and transport. Clustered, placebo-permutation and collapsed two-period estimates and sensitivity analyses in online supplemental table S3.'}
ev=pd.read_csv(O+'t24_events_2016_2025.csv',index_col=0); ev.columns=ev.columns.astype(int)
lab=[('Harassment','Harassment',True),('Power harassment by supervisors','\u2003Power harassment\u2020',False),('Bullying or violence (co-workers)','\u2003Bullying/violence\u2021',False),('Sexual harassment','\u2003Sexual harassment',False),('Customer harassment','\u2003Customer harassment\u00a7',False),
     ('Change in workload','Workload change',True),('Working hours','Working hours\u00b6',True),('Accidents, disasters, injury','Accidents/injury',True),('Special events','Special events',True),('Other','Other',True),('Total','Total',True)]
yrs=list(range(2016,2026)); rows3=[]
for k,name,share in lab:
    v=ev.loc[k]; cells=[('–' if pd.isna(v[y]) else str(int(v[y]))) for y in yrs]
    sh=lambda y: '–' if (pd.isna(v[y]) or not share or k=='Total') else f"{v[y]/ev.loc['Total',y]*100:.0f}"
    d=v[2024]-v[2022] if not (pd.isna(v[2024]) or pd.isna(v[2022])) else (v[2024] if k=='Customer harassment' else np.nan)
    dch='–' if pd.isna(d) else f"{int(d):+d}"
    rows3.append([('**Total**' if k=='Total' else name)]+cells+[sh(2016) if k!='Total' else '100',sh(2025) if k!='Total' else '100',dch])
tab3={'title':[['Table 3',1,0],[' Approved claims for mental disorders by precipitating event, FY2016–2025',0,0]],
 'groups':[['',1],['Approved claims, n',10],['Share, %',2],['',1]],'header':['Event group']+[f"'{str(y)[2:]}" for y in yrs]+['2016','2025','\u0394 22–24'],
 'rows':rows3,'widths':[1826]+[540]*10+[550,550,700],'font':15,
 'note':'FY, fiscal year, April to March (\u201916 = FY2016, April 2016–March 2017). \u0394 22–24, change in approved claims between FY2022, the last fiscal year decided wholly under the May 2020 criteria, and FY2024, the first decided wholly under the September 2023 criteria (total +346); this interval contains the largest two-year increase of the decade. \u2020Recognised as a separate event from May 2020; before then included under bullying/violence or conflict with supervisors. \u2021Before May 2020, \u201csevere harassment, bullying or violence\u201d (including by supervisors). \u00a7Listed as a precipitating event in the compensation criteria from September 2023; an employer duty to prevent customer harassment took effect on 1 October 2026, after the study period. \u00b6\u226580 hours of overtime in a month or \u22652 weeks of continuous work. FY2016–2019 follow the 2011 recognition criteria; categories are not fully comparable across the May 2020 and September 2023 revisions.'}
tables=[tab1,tab2,tab3]
legs={}
for m in re.finditer(r'\*\*(Figure \d)\*\* (.*)',legsec): legs[m.group(1)]=m.group(2)
supp_line=[l for l in legsec.split('\n') if l.startswith(('**Online','**Supplementary'))][0]
figs=[{'title':'Figure 1','legend':legs['Figure 1'],'path':'output/figures/Figure1.png','px':list(__import__('PIL.Image',fromlist=['Image']).open('output/figures/Figure1.png').size)},
      {'title':'Figure 2','legend':legs['Figure 2'],'path':'output/figures/Figure2.png','px':list(__import__('PIL.Image',fromlist=['Image']).open('output/figures/Figure2.png').size)}]
json.dump({'blocks':blocks,'tables':tables,'figs':figs,'supp_line':runs(supp_line)},open(O+'spec_main.json','w'),ensure_ascii=False)

# ---------------- supplementary ----------------
def df_table(df):
    h=list(df.columns); r=[[str(x) for x in row] for row in df.values]; return h,r
st=[]
s1=pd.read_csv(S+'TableS1.csv'); h,r=df_table(s1)
st.append({'title':[['Table S1',1,0],[' Transcription checks: transcribed counts compared with published national totals, FY2016–2025',0,0]],'header':h,'rows':r,'widths':widths(h,r,total=13900,minw=1100),'font':15,'landscape':True,
 'note':'Industry-level counts were transcribed from the MHLW annual reports (each lists the current and the previous fiscal year; overlapping years were cross-checked, and approvals were also checked against an MHLW committee compilation); prefecture-level counts are available from FY2021. CVD, cerebro-cardiovascular diseases. Reports no longer hosted by the ministry (FY2019–FY2021) were retrieved from the Internet Archive; the FY2024 prefecture table (image only) was transcribed manually. "–", not transcribed. All transcribed series sum exactly to the published national totals.'})
s5=pd.read_csv(S+'TableS5_eventstudy_pooled.csv'); h,r=df_table(s5)
st.append({'title':[['Table S2',1,0],[' Event studies for the two natural experiments, relative to the mean of each experiment\u2019s pre-cap period',0,0]],'header':h,'rows':r,'widths':[1500,700,1500,1776,1776,1776],'font':15,
 'note':'Experiment 1 (April 2019/2020 cap): six comparison industries (newly capped) vs construction and transport, FY2016–2023, reference = mean of FY2016–2018. Experiment 2 (April 2024 cap): construction and transport (newly capped) vs six comparison industries, FY2020–2025 (FY2020 is the first year in which all six control industries were capped), reference = mean of FY2021–2023. Each IRR is the deviation of that year from the pre-cap mean (delta method), so every year, including reference years, has a CI. Poisson regression with industry and year fixed effects, newly capped group × year interactions, log employed persons as offset and HC1 standard errors. MD, mental disorders; CVD, cerebro-cardiovascular diseases (positive control for exposure). MD and CVD approvals are plotted in figure 2.'})
s7=pd.read_csv(S+'TableS7_sensitivity.csv'); s7['Contrast']=s7['Contrast'].map({'2024 cap':'Experiment 2','2019–20 cap':'Experiment 1'}); s7=s7.sort_values('Contrast',kind='stable'); h=list(s7.columns); r=[[str(x) for x in row] for row in s7.values]
_inf=pd.read_csv(S+'TableS3b_inference.csv'); _inf=_inf[~_inf['Inference / specification'].str.startswith('Main: HC1')]
_inf2=pd.DataFrame({'Contrast':_inf['Contrast'],'Specification':_inf['Inference / specification'],'Outcome':_inf['Outcome'],'IRR (95% CI)':_inf['IRR (95% CI)'],'p':_inf['p']})
_emp=pd.read_csv(S+'TableS3c_employees_denominator.csv'); _emp=_emp[_emp['Denominator']=='Employees']
_emp2=pd.DataFrame({'Contrast':_emp['Contrast'],'Specification':'Employees as denominator, wild cluster score bootstrap','Outcome':_emp['Outcome'],'IRR (95% CI)':_emp['IRR (95% CI), wild cluster bootstrap'],'p':_emp['p (wild)']})
s7=pd.concat([s7,_inf2,_emp2],ignore_index=True); r=[[str(x) for x in row] for row in s7.values]
pl=open(S+'placebo.txt').read()
st.append({'title':[['Table S3',1,0],[' Sensitivity analyses and small-cluster inference for the difference-in-differences estimates',0,0]],'header':h,'rows':r,'widths':[1400,3600,1300,1926,800],
 'note':'All models: Poisson regression with industry and year fixed effects and log employed persons as offset; HC1 standard errors unless the specification states another method of inference. Clustered: standard errors clustered by industry (eight clusters) with t(7) critical values. Wild cluster score bootstrap (primary method of inference): Kline and Santos score bootstrap clustered by industry with Webb six-point weights (9999 draws), p value at IRR=1 and 95% CI by test inversion; it may be unreliable because only two industries were newly capped (experiment 2) or served as controls (experiment 1). Placebo permutation: the treatment label assigned to each of the 28 possible pairs of the eight industries; CI by test inversion (computed for approvals only); because the caps were not randomly assigned, these p values are descriptive and not those of a randomization test. Clustered, placebo permutation and collapsed estimates are sensitivity analyses; the collapsed models use HC1 standard errors with only 16 observations and should not be given more weight than the bootstrap. Collapsed: counts and employment summed within each industry for the pre-cap and post-cap periods (16 observations). Employees as denominator: employees (excluding the self-employed and family workers, who are not covered by workers’ compensation insurance) from the Labour Force Survey, 2025 annual average results, table I-8, replace employed persons in the offset; the non-employee share was 11.3–12.4% in construction and transport and 5.6–6.8% in the six comparison industries in FY2016–2025. Experiment 2 (April 2024 cap): construction and transport treated, FY2021–2023 vs FY2024–2025 unless stated. Experiment 1 (April 2019/2020 cap): six comparison industries treated, FY2016–2018 vs FY2019–2023 unless stated; construction and transport as controls. Permutation test for experiment 2: the main model was re-estimated with each of the 28 possible pairs of the eight industries as placebo-treated; placebo IRRs ranged from 0.79 to 1.15, half were below 1, and the observed estimate (1.10) had a two-sided permutation p value of 0.36. CVD, cerebro-cardiovascular diseases (positive control for exposure).'})
s3=pd.read_csv(S+'TableS3.csv'); s3['IRR (95% CI)']=s3['IRR (95% CI)'].str.replace(r' p=.*','',regex=True)
t14=pd.read_csv(O+'t14_pref_did.csv'); pv=t14['IRR (95%CI)'].str.extract(r'p=([\d.]+)')[0].fillna('–')
s3['p']=pv.values; h,r=df_table(s3)
st.append({'title':[['Table S4',1,0],[' Prefecture panel: Poisson models of approvals and claims for mental disorders (47 prefectures × FY2021–2025)',0,0]],'header':h,'rows':r,'widths':widths(h,r,first=40),
 'note':'IRR, incidence rate ratio per SD of exposure (standardised 2015 share of employment in construction and transport). All models include prefecture and year fixed effects and log employed persons as offset; standard errors clustered by prefecture. Event-study rows use FY2021 as reference.'})

strobe=[
('Title and abstract','1','(a) Indicate the study’s design with a commonly used term in the title or the abstract; (b) provide an informative and balanced summary','Title (“natural experiments”); Abstract'),
('Background/rationale','2','Explain the scientific background and rationale','Introduction, paragraphs 1–3'),
('Objectives','3','State specific objectives, including any prespecified hypotheses','Introduction, paragraph 3; Abstract (Objectives)'),
('Study design','4','Present key elements of study design early in the paper','Methods: Design and data'),
('Setting','5','Describe the setting, locations and relevant dates','Methods: Design and data; Two natural experiments (Japan, FY2016–2025; caps April 2019/2020 and April 2024)'),
('Participants','6','Give the eligibility criteria and sources and methods of selection','Methods: Design and data; Two natural experiments (all compensation decisions; industry selection)'),
('Variables','7','Clearly define all outcomes, exposures, predictors, potential confounders and effect modifiers','Methods: Two natural experiments; Statistical analysis (outcomes: claims, approvals; positive control for exposure: cerebro-cardiovascular, both caps)'),
('Data sources/measurement','8*','For each variable, give sources of data and details of methods of assessment','Methods: Design and data; table 1; table S1'),
('Bias','9','Describe any efforts to address potential sources of bias','Methods: Statistical analysis (separate contrasts, event study, positive control for exposure, permutation test, sensitivity analyses, prefecture panel); Discussion: Were the caps complied with?'),
('Study size','10','Explain how the study size was arrived at','Methods: Design and data (complete national data; 9 industries × 10 years, 47 prefectures × 5 years)'),
('Quantitative variables','11','Explain how quantitative variables were handled in the analyses','Methods: Statistical analysis (rates per million; standardised prefecture exposure)'),
('Statistical methods','12','(a) Describe all statistical methods, including those used to control for confounding; (b) subgroups and interactions; (c) missing data; (d) sampling strategy; (e) sensitivity analyses','Methods: Statistical analysis; table 2; tables S2–S4'),
('Participants','13*','Report numbers of individuals at each stage of study','Not applicable (aggregate administrative counts); counts reported in tables 1 and 3 and table S1'),
('Descriptive data','14*','Give characteristics of study participants and information on exposures and potential confounders','Results: Ten-year trends; table 1; figure 1'),
('Outcome data','15*','Report numbers of outcome events or summary measures','Table 1; table 3; figure 1; table S1'),
('Main results','16','(a) Give unadjusted estimates and, if applicable, confounder-adjusted estimates and their precision (eg, 95% CI)','Results: Experiment 1; Experiment 2; table 2; figure 2'),
('Other analyses','17','Report other analyses done—eg, analyses of subgroups and interactions, and sensitivity analyses','Results: Robustness; Precipitating events; tables S2–S4'),
('Key results','18','Summarise key results with reference to study objectives','Discussion: Principal findings'),
('Limitations','19','Discuss limitations, taking into account sources of potential bias or imprecision','Discussion: Were the caps complied with?; Strengths and limitations'),
('Interpretation','20','Give a cautious overall interpretation of results','Discussion: Other explanations; Comparison with other studies; Implications; Conclusion'),
('Generalisability','21','Discuss the generalisability (external validity) of the study results','Discussion: Strengths and limitations; Implications'),
('Funding','22','Give the source of funding and the role of the funders','Funding statement (none)'),
]
h=['Section/topic','Item','Recommendation (abridged)','Reported in']; r=[list(x) for x in strobe]
st.append({'title':[['STROBE checklist',1,0],[' (cross-sectional/ecological study items)',0,0]],'header':h,'rows':r,'widths':[1800,600,3626,3000],
 'note':'*Items 8 and 13–15 apply to aggregate counts rather than individual participants. Checklist adapted from von Elm et al., Lancet 2007;370:1453–7.'})
sf=[]
title=md.split('\n')[0][2:]
json.dump({'title':title,'tables':st,'figs':sf},open(O+'spec_supp.json','w'),ensure_ascii=False)
print(len(blocks),'blocks;',[t['widths'] for t in tables])
