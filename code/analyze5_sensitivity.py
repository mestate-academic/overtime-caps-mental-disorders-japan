# -*- coding: utf-8 -*-
"""Reviewer-driven sensitivity analyses + descriptive Table 1 for v4"""
import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf, itertools
O='output/intermediate/'; S='output/tables/'
d=pd.read_csv(O+'t6_industry_rates.csv'); dd=d[d.med==0].copy()
EN={'製造業':'Manufacturing','建設業':'Construction','運輸業郵便業':'Transport and postal services','卸売小売業':'Wholesale and retail','金融保険業':'Finance and insurance','教育学習支援業':'Education','医療福祉':'Health care and welfare','情報通信業':'Information and communication','宿泊飲食':'Accommodation and food services'}
def fit(df,y,term,off='emp'):
    m=smf.glm(f'{y} ~ C(industry)+C(fy)+{term}',data=df,family=sm.families.Poisson(),offset=np.log(df[off])).fit(cov_type='HC1')
    b=m.params[term]; lo,hi=m.conf_int().loc[term]; return np.exp(b),np.exp(lo),np.exp(hi),m.pvalues[term]
def fmt(r): return f'{r[0]:.2f} ({r[1]:.2f} to {r[2]:.2f})', ('<0.001' if r[3]<0.001 else f'{r[3]:.3f}' if r[3]<0.01 else f'{r[3]:.2f}')
rows=[]
# --- 2024 cap main & sensitivity
d2=dd[dd.fy>=2021].copy(); d2['post24']=(d2.fy>=2024).astype(int)
rows.append(['2024 cap','Main (FY2021–25, 6 controls)','Approvals']+list(fmt(fit(d2,'approvals','late:post24'))))
d2b=d2[d2.industry!='宿泊飲食']; rows.append(['2024 cap','Excluding accommodation and food services','Approvals']+list(fmt(fit(d2b,'approvals','late:post24'))))
d2c=d2[d2.fy!=2023].copy(); rows.append(['2024 cap','Excluding FY2023 (anticipation year)','Approvals']+list(fmt(fit(d2c,'approvals','late:post24'))))
d2d=dd[dd.fy>=2016].copy(); d2d['post24']=(d2d.fy>=2024).astype(int); rows.append(['2024 cap','Longer pre-period (FY2016–25)','Approvals']+list(fmt(fit(d2d,'approvals','late:post24'))))
# treat each exempted industry separately
for ind in ['建設業','運輸業郵便業']:
    dx=d2[(d2.late==0)|(d2.industry==ind)].copy(); dx['t']=(dx.industry==ind).astype(int)
    rows.append(['2024 cap',f'{EN[ind]} only vs 6 controls','Approvals']+list(fmt(fit(dx,'approvals','t:post24'))))
# --- 2019 cap main & sensitivity
d3=dd[(dd.fy>=2016)&(dd.fy<=2023)].copy(); d3['post19']=(d3.fy>=2019).astype(int); d3['general']=1-d3.late
rows.append(['2019–20 cap','Main (FY2016–23)','Approvals']+list(fmt(fit(d3,'approvals','general:post19'))))
d3b=d3[d3.fy<=2022]; rows.append(['2019–20 cap','Excluding FY2023 (anticipation in controls)','Approvals']+list(fmt(fit(d3b,'approvals','general:post19'))))
d3c=d3[~d3.fy.isin([2020,2021])]; rows.append(['2019–20 cap','Excluding FY2020–21 (COVID-19)','Approvals']+list(fmt(fit(d3c,'approvals','general:post19'))))
d3d=d3[d3.industry!='宿泊飲食']; rows.append(['2019–20 cap','Excluding accommodation and food services','Approvals']+list(fmt(fit(d3d,'approvals','general:post19'))))
rows.append(['2019–20 cap','Main (FY2016–23)','Claims']+list(fmt(fit(d3,'claims','general:post19'))))
rows.append(['2019–20 cap','Excluding FY2023','Claims']+list(fmt(fit(d3b,'claims','general:post19'))))
rows.append(['2019–20 cap','Positive control, main (FY2016–23)','CVD approvals']+list(fmt(fit(d3,'cvd_approvals','general:post19'))))
rows.append(['2019–20 cap','Positive control, excluding FY2023','CVD approvals']+list(fmt(fit(d3b,'cvd_approvals','general:post19'))))
rows.append(['2019–20 cap','Positive control, main (FY2016–23)','CVD claims']+list(fmt(fit(d3,'cvd_claims','general:post19'))))
rows.append(['2024 cap','Positive control, longer pre-period (FY2016–25)','CVD approvals']+list(fmt(fit(d2d,'cvd_approvals','late:post24'))))
rows.append(['2024 cap','Positive control, longer pre-period (FY2016–25)','CVD claims']+list(fmt(fit(d2d,'cvd_claims','late:post24'))))
rows.append(['2024 cap','Claims, longer pre-period (FY2016–25)','Claims']+list(fmt(fit(d2d,'claims','late:post24'))))
# health care and welfare (physicians capped April 2024) added to the newly capped group in experiment 2
dh=d[d.fy>=2021].copy(); dh['post24']=(dh.fy>=2024).astype(int); dh['t']=((dh.late==1)|(dh.med==1)).astype(int)
rows.append(['2024 cap','Health care and welfare added to construction & transport (post hoc)','Approvals']+list(fmt(fit(dh,'approvals','t:post24'))))
dh2=dh[dh.late==0].copy(); dh2['t']=dh2.med
rows.append(['2024 cap','Health care and welfare only vs 6 controls (post hoc)','Approvals']+list(fmt(fit(dh2,'approvals','t:post24'))))
# experiment 1 excluding FY2019 transition year (only large firms capped) (post hoc)
dx=dd[(dd.fy>=2016)&(dd.fy<=2023)&(dd.fy!=2019)].copy(); dx['post19']=(dx.fy>=2020).astype(int); dx['general']=1-dx.late
rows.append(['2019–20 cap','Excluding FY2019, transition year (post hoc)','Approvals']+list(fmt(fit(dx,'approvals','general:post19'))))
# alternative pre-periods for experiment 2 (post hoc)
for a in [2019,2020]:
    dp=dd[dd.fy>=a].copy(); dp['post24']=(dp.fy>=2024).astype(int)
    rows.append(['2024 cap',f'Pre-period FY{a}–23 (post hoc)','Approvals']+list(fmt(fit(dp,'approvals','late:post24'))))
# CVD event study FY2016-25, ref FY2023
ec=dd[dd.fy>=2016].copy(); yrs=sorted(ec.fy.unique())
for y in yrs:
    if y!=2023: ec[f'ev_{y}']=((ec.fy==y)&(ec.late==1)).astype(int)
mm2=smf.glm('cvd_approvals ~ C(industry)+C(fy)+'+'+'.join(f'ev_{y}' for y in yrs if y!=2023),data=ec,family=sm.families.Poisson(),offset=np.log(ec.emp)).fit(cov_type='HC1')
mm3=smf.glm('claims ~ C(industry)+C(fy)+'+'+'.join(f'ev_{y}' for y in yrs if y!=2023),data=ec,family=sm.families.Poisson(),offset=np.log(ec.emp)).fit(cov_type='HC1')
f=lambda m,y: '1 (reference)' if y==2023 else '%.2f (%.2f to %.2f)'%(np.exp(m.params[f'ev_{y}']),*np.exp(m.conf_int().loc[f'ev_{y}']))
esc=pd.DataFrame({'FY':yrs,'CVD approvals, IRR (95% CI)':[f(mm2,y) for y in yrs],'Mental-disorder claims, IRR (95% CI)':[f(mm3,y) for y in yrs]})
esc.to_csv(S+'TableS8_eventstudy_cvd_claims.csv',index=False); print(esc.to_string())
pd.DataFrame({'fy':yrs,'IRR':[1 if y==2023 else np.exp(mm2.params[f'ev_{y}']) for y in yrs],'lo':[1 if y==2023 else np.exp(mm2.conf_int().loc[f'ev_{y}'][0]) for y in yrs],'hi':[1 if y==2023 else np.exp(mm2.conf_int().loc[f'ev_{y}'][1]) for y in yrs]}).to_csv(O+'t23_es_cvd.csv',index=False)
# --- permutation / placebo: 2024 cap, every pair of the 8 industries as pseudo-treated
inds=sorted(d2.industry.unique()); act=fit(d2,'approvals','late:post24')[0]; pl=[]
for pair in itertools.combinations(inds,2):
    dx=d2.copy(); dx['t']=dx.industry.isin(pair).astype(int); pl.append((pair,fit(dx,'approvals','t:post24')[0]))
vals=np.array([v for _,v in pl]); rank=(np.abs(np.log(vals))>=abs(np.log(act))).mean()
perm_txt=f'Placebo distribution over all {len(pl)} pairs of industries: actual log-IRR ranked with permutation p={rank:.2f}; placebo IRR range {vals.min():.2f}–{vals.max():.2f}; share of placebo IRR<1: {(vals<1).mean():.2f}'
print(perm_txt)
# event study ref 2022
years=sorted(dd[dd.fy>=2016].fy.unique()); e22=dd[dd.fy>=2016].copy()
for y in years:
    if y!=2022: e22[f'ev_{y}']=((e22.fy==y)&(e22.late==1)).astype(int)
form='approvals ~ C(industry)+C(fy)+'+'+'.join(f'ev_{y}' for y in years if y!=2022)
m=smf.glm(form,data=e22,family=sm.families.Poisson(),offset=np.log(e22.emp)).fit(cov_type='HC1')
es22=pd.DataFrame({'FY':years,'IRR (95% CI), ref. FY2022':[ '1 (reference)' if y==2022 else '%.2f (%.2f to %.2f)'%(np.exp(m.params[f'ev_{y}']),*np.exp(m.conf_int().loc[f'ev_{y}'])) for y in years]})
es22.to_csv(S+'TableS6_eventstudy_ref2022.csv',index=False); print(es22)
e23=dd[dd.fy>=2016].copy()
for y in years:
    if y!=2023: e23[f'ev_{y}']=((e23.fy==y)&(e23.late==1)).astype(int)
m23=smf.glm('approvals ~ C(industry)+C(fy)+'+'+'.join(f'ev_{y}' for y in years if y!=2023),data=e23,family=sm.families.Poisson(),offset=np.log(e23.emp)).fit(cov_type='HC1')
t8=pd.DataFrame({'fy':years,'IRR':[1.0 if y==2023 else np.exp(m23.params[f'ev_{y}']) for y in years],'lo':[1.0 if y==2023 else np.exp(m23.conf_int().loc[f'ev_{y}'][0]) for y in years],'hi':[1.0 if y==2023 else np.exp(m23.conf_int().loc[f'ev_{y}'][1]) for y in years]})
t8.to_csv(O+'t8_event_study_offset.csv',index=False); print(t8.round(2))
sens=pd.DataFrame(rows,columns=['Contrast','Specification','Outcome','IRR (95% CI)','p']); sens.to_csv(S+'TableS7_sensitivity.csv',index=False); print(sens.to_string())
open(S+'placebo.txt','w').write(perm_txt)

# --- descriptive Table 1: characteristics of the industries (analytic units)
def agg(df,fys,col): return df[df.fy.isin(fys)].groupby('industry')[col].sum()
emp23=d[d.fy==2023].set_index('industry').emp/1e6
t1=pd.DataFrame({'emp23':emp23,
 'app1618':agg(d,range(2016,2019),'approvals'),'app1923':agg(d,range(2019,2024),'approvals'),'app2123':agg(d,range(2021,2024),'approvals'),'app2425':agg(d,range(2024,2026),'approvals'),
 'cl1618':agg(d,range(2016,2019),'claims'),'cl1923':agg(d,range(2019,2024),'claims'),'cvd1618':agg(d,range(2016,2019),'cvd_approvals'),'cvd1923':agg(d,range(2019,2024),'cvd_approvals'),'cl2123':agg(d,range(2021,2024),'claims'),'cl2425':agg(d,range(2024,2026),'claims'),'cvd2123':agg(d,range(2021,2024),'cvd_approvals'),'cvd2425':agg(d,range(2024,2026),'cvd_approvals')})
emp_mean=lambda fys: d[d.fy.isin(fys)].groupby('industry').emp.mean()
t1['r1618']=t1.app1618/3/emp_mean(range(2016,2019))*1e6; t1['r1923']=t1.app1923/5/emp_mean(range(2019,2024))*1e6; t1['r2123']=t1.app2123/3/emp_mean(range(2021,2024))*1e6; t1['r2425']=t1.app2425/2/emp_mean(range(2024,2026))*1e6
order=['建設業','運輸業郵便業','製造業','卸売小売業','金融保険業','教育学習支援業','情報通信業','宿泊飲食','医療福祉']
grp={'建設業':'Exempted until 2024','運輸業郵便業':'Exempted until 2024','医療福祉':'Partly exempted (physicians); excluded from main contrast'}
out=[]
for i in order:
    r=t1.loc[i]; out.append([EN[i],grp.get(i,'Regulated from 2019–20 (comparison)'),f'{r.emp23:.2f}',int(r.cl1618),int(r.cl1923),int(r.cl2425),int(r.app1618),int(r.app1923),int(r.app2425),int(r.cvd1618),int(r.cvd1923),int(r.cvd2425),f'{r.r1618:.1f}',f'{r.r1923:.1f}',f'{r.r2425:.1f}'])
T1=pd.DataFrame(out,columns=['Industry','Status','Employed, millions (2023)','Claims FY2016–18','Claims FY2019–23','Claims FY2024–25','Approvals FY2016–18','Approvals FY2019–23','Approvals FY2024–25','CVD approvals FY2016–18','CVD approvals FY2019–23','CVD approvals FY2024–25','Approval rate FY2016–18','Approval rate FY2019–23','Approval rate FY2024–25'])
T1.to_csv(S+'Table1_descriptive.csv',index=False); print(T1.to_string())
# group totals
for g,ids in [('Exempted (2)',['建設業','運輸業郵便業']),('Non-exempted (6)',[i for i in order if i not in ['建設業','運輸業郵便業','医療福祉']])]:
    r=t1.loc[ids].sum(); em0=emp_mean(range(2016,2019)).loc[ids].sum(); em=emp_mean(range(2019,2024)).loc[ids].sum(); em2=emp_mean(range(2024,2026)).loc[ids].sum()
    tot=[g,'',f'{r.emp23:.2f}',int(r.cl1618),int(r.cl1923),int(r.cl2425),int(r.app1618),int(r.app1923),int(r.app2425),int(r.cvd1618),int(r.cvd1923),int(r.cvd2425),f'{r.app1618/3/em0*1e6:.1f}',f'{r.app1923/5/em*1e6:.1f}',f'{r.app2425/2/em2*1e6:.1f}']
    print('TOTAL',tot); pd.DataFrame([tot]).to_csv(S+f'T1_total_{g[:3]}.csv',index=False)
