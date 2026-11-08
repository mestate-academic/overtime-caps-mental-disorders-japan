# -*- coding: utf-8 -*-
"""Event studies for the two natural experiments, each relative to the mean of its own pre-cap period.
Exp 1 (cap from April 2019 large firms / April 2020 SMEs): six industries (treated) vs construction & transport,
       FY2016-2023, reference = mean of FY2016-2018.
Exp 2 (cap from April 2024): construction & transport (treated) vs six industries,
       FY2020-2025 (FY2020 = first year in which all six control industries were capped), reference = mean of FY2021-2023.
Every year gets an estimate and a 95% CI (deviation from the pooled pre-period baseline; delta method)."""
import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf
O='output/intermediate/'; S='output/tables/'
d=pd.read_csv(O+'t6_industry_rates.csv'); dd=d[d.med==0].copy()

def es(df,treat,y,years,ref):
    df=df[df.fy.isin(years)].copy(); base=years[0]
    for t in years:
        if t!=base: df[f'ev_{t}']=((df.fy==t)&(df[treat]==1)).astype(int)
    m=smf.glm(f'{y} ~ C(industry)+C(fy)+'+'+'.join(f'ev_{t}' for t in years if t!=base),data=df,
              family=sm.families.Poisson(),offset=np.log(df.emp)).fit(cov_type='HC1')
    names=list(m.params.index); V=m.cov_params().values; b=m.params.values; out=[]
    for t in years:
        L=np.zeros(len(names))
        if t!=base: L[names.index(f'ev_{t}')]+=1
        for r in ref:
            if r!=base: L[names.index(f'ev_{r}')]-=1/len(ref)
        est=L@b; se=np.sqrt(L@V@L)
        out.append({'fy':t,'IRR':np.exp(est),'lo':np.exp(est-1.96*se),'hi':np.exp(est+1.96*se)})
    return pd.DataFrame(out)

dd['six']=1-dd.late
E={1:dict(treat='six',years=list(range(2016,2024)),ref=[2016,2017,2018]),
   2:dict(treat='late',years=list(range(2020,2026)),ref=[2021,2022,2023])}
rows=[]
for k,cfg in E.items():
    for y in ['approvals','claims','cvd_approvals']:
        r=es(dd,cfg['treat'],y,cfg['years'],cfg['ref']); r['exp']=k; r['outcome']=y; rows.append(r)
R=pd.concat(rows); R.to_csv(O+'t25_es_pooled.csv',index=False)
f=lambda r:f'{r.IRR:.2f} ({r.lo:.2f} to {r.hi:.2f})'
tab=[]
for k in [1,2]:
    for t in E[k]['years']:
        x=R[(R.exp==k)&(R.fy==t)].set_index('outcome')
        tab.append([f'Experiment {k}',t,'Reference period' if t in E[k]['ref'] else ('After cap' if (k==1 and t>=2019) or (k==2 and t>=2024) else 'Before cap'),
                    f(x.loc['approvals']),f(x.loc['claims']),f(x.loc['cvd_approvals'])])
T=pd.DataFrame(tab,columns=['Experiment','FY','Period','MD approvals, IRR (95% CI)','MD claims, IRR (95% CI)','CVD approvals, IRR (95% CI)'])
T.to_csv(S+'TableS5_eventstudy_pooled.csv',index=False); print(T.to_string())
