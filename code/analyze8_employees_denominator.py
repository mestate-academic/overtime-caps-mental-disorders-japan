# -*- coding: utf-8 -*-
"""Sensitivity analysis (reviewer request): employees instead of employed persons as the denominator.

Employed persons include the self-employed and family workers, who are not covered by workers'
compensation insurance and are numerous in construction. Here the offset is log(employees) from
data/employees_by_industry.csv (Labour Force Survey, table I-8). Main Poisson DiD with HC1 SEs and the
wild cluster score bootstrap (same functions and seed as analyze7_inference.py).
"""
import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf
O='output/intermediate/'; S='output/tables/'
d=pd.read_csv(O+'t6_industry_rates.csv')
e=pd.read_csv('data/employees_by_industry.csv').melt(id_vars='year',var_name='industry',value_name='employees')
e['employees']*=1e4
d=d.merge(e,left_on=['fy','industry'],right_on=['year','industry'],how='left')
assert d.loc[d.fy>=2016,'employees'].notna().all()
dd=d[d.med==0].copy()
rng=np.random.default_rng(20261108)
WEBB=np.array([-np.sqrt(1.5),-1,-np.sqrt(.5),np.sqrt(.5),1,np.sqrt(1.5)]); B=9999
W8=rng.choice(WEBB,size=(B,8))

def setup(exp,y):
    if exp==1:
        df=dd[(dd.fy>=2016)&(dd.fy<=2023)].copy(); df['post']=(df.fy>=2019).astype(int); df['tr']=1-df.late
    else:
        df=dd[dd.fy>=2021].copy(); df['post']=(df.fy>=2024).astype(int); df['tr']=df.late
    return df.dropna(subset=[y]).reset_index(drop=True)

def design(df):
    X=pd.get_dummies(df[['industry','fy']].astype(str),drop_first=True).astype(float)
    X.insert(0,'const',1.0); X['D']=(df['tr']*df['post']).values.astype(float)
    return X.values, list(X.columns)

def score_stat(df,y,b0,X,cols,den):
    jD=cols.index('D'); Xg=np.delete(X,jD,axis=1)
    off=np.log(df[den].values)+b0*X[:,jD]
    r=sm.GLM(df[y].values,Xg,family=sm.families.Poisson(),offset=off).fit()
    mu=r.mu; res=df[y].values-mu; H=(X*mu[:,None]).T@X
    jo=[k for k in range(X.shape[1]) if k!=jD]; proj=H[jD,jo]@np.linalg.pinv(H[np.ix_(jo,jo)])
    g=pd.factorize(df.industry)[0]; s=np.zeros(g.max()+1)
    for k in range(g.max()+1):
        idx=g==k; Sg=X[idx].T@res[idx]; s[k]=Sg[jD]-proj@Sg[jo]
    return s

def wild_p(df,y,b0,X,cols,W,den):
    s=score_stat(df,y,b0,X,cols,den); T=s.sum()/np.sqrt((s**2).sum())
    Ts=(W*s).sum(1)/np.sqrt(((W*s)**2).sum(1)); return np.mean(np.abs(Ts)>=abs(T)-1e-12)

def invert(pf,b,se):
    grid=np.linspace(b-6*se,b+6*se,241); ps=np.array([pf(x) for x in grid]); a=grid[ps>.05]
    return (a.min(),a.max()) if len(a) else (np.nan,np.nan)

fmt=lambda e,l,h: f'{e:.2f} ({l:.2f} to {h:.2f})'
fp=lambda p: '<0.001' if p<0.001 else f'{p:.3f}' if p<0.01 else f'{p:.2f}'
rows=[]; summ={}
for exp in (1,2):
    for y,lab in [('approvals','Approvals'),('claims','Claims'),('cvd_approvals','CVD approvals'),('cvd_claims','CVD claims')]:
        df=setup(exp,y)
        for den,dlab in [('emp','Employed persons (main)'),('employees','Employees')]:
            m=smf.glm(f'{y} ~ C(industry)+C(fy)+tr:post',data=df,family=sm.families.Poisson(),offset=np.log(df[den])).fit(cov_type='HC1')
            b=m.params['tr:post']; se=m.bse['tr:post']; ci=np.exp(m.conf_int().loc['tr:post'])
            sec=smf.glm(f'{y} ~ C(industry)+C(fy)+tr:post',data=df,family=sm.families.Poisson(),offset=np.log(df[den])).fit(cov_type='cluster',cov_kwds={'groups':pd.factorize(df.industry)[0]}).bse['tr:post']
            X,cols=design(df); W=W8[:,:df.industry.nunique()]
            pw=wild_p(df,y,0.0,X,cols,W,den); lo,hi=invert(lambda x: wild_p(df,y,x,X,cols,W,den),b,max(se,sec))  # same grid as analyze7
            rows.append([f'Experiment {exp}',lab,dlab,fmt(np.exp(b),*ci),fmt(np.exp(b),np.exp(lo),np.exp(hi)),fp(pw)])
            summ[(exp,y,den)]=dict(irr=np.exp(b),hc1=list(ci),wild=[np.exp(lo),np.exp(hi)],p=pw)
            print(rows[-1],flush=True)
# self-employed share (1 - employees/employed) by group and year
sh=dd[dd.fy>=2016].assign(g=lambda x: np.where(x.late==1,'Construction and transport','Six comparison industries')).groupby(['g','fy'])[['emp','employees']].sum()
sh['non_employee_share_pct']=(100*(1-sh.employees/sh.emp)).round(1)
sh=sh.reset_index()[['g','fy','non_employee_share_pct']]; print(sh.pivot(index='fy',columns='g').to_string())
T=pd.DataFrame(rows,columns=['Contrast','Outcome','Denominator','IRR (95% CI), HC1','IRR (95% CI), wild cluster bootstrap','p (wild)'])
T.to_csv(S+'TableS3c_employees_denominator.csv',index=False)
sh.to_csv(S+'TableS3c_nonemployee_share.csv',index=False)
pd.to_pickle(summ,O+'employees_summary.pkl')
