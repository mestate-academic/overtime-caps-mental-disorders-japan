# -*- coding: utf-8 -*-
"""Small-cluster inference for the main difference-in-differences estimates.

For each experiment and outcome, the main Poisson DiD estimate is re-assessed with:
  (1) standard errors clustered by industry (CR1) with t(G-1) critical values;
  (2) wild cluster score bootstrap (Kline & Santos 2012) with Webb six-point weights,
      p-value and 95% CI by test inversion (9999 draws);
  (3) placebo permutation analysis over all 28 assignments of the treatment label (test inversion
      for the 95% CI);
  (4) the panel collapsed to one pre and one post period per industry (Bertrand et al. 2004).
Also: sensitivity excluding the two control industries most exposed to customer harassment.
"""
import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf, itertools
from scipy import stats
O='output/intermediate/'; S='output/tables/'
d=pd.read_csv(O+'t6_industry_rates.csv'); dd=d[d.med==0].copy()
rng=np.random.default_rng(20261108)
WEBB=np.array([-np.sqrt(1.5),-1,-np.sqrt(.5),np.sqrt(.5),1,np.sqrt(1.5)])
B=9999

def design(df,treat):
    X=pd.get_dummies(df[['industry','fy']].astype(str),drop_first=True).astype(float)
    X.insert(0,'const',1.0); X['D']=(df[treat]*df['post']).values.astype(float)
    return X.values, list(X.columns)

def setup(exp,y):
    if exp==1:
        df=dd[(dd.fy>=2016)&(dd.fy<=2023)].copy(); df['post']=(df.fy>=2019).astype(int); df['tr']=1-df.late
    else:
        df=dd[dd.fy>=2021].copy(); df['post']=(df.fy>=2024).astype(int); df['tr']=df.late
    df=df.dropna(subset=[y]).reset_index(drop=True); return df

def fit_glm(df,y,cov='HC1',groups=None):
    m=smf.glm(f'{y} ~ C(industry)+C(fy)+tr:post',data=df,family=sm.families.Poisson(),offset=np.log(df.emp))
    if cov=='cluster': r=m.fit(cov_type='cluster',cov_kwds={'groups':pd.factorize(df.industry)[0]})
    else: r=m.fit(cov_type=cov)
    return r

def score_stat(df,y,b0,X,cols,w=None):
    """Restricted fit under beta=b0, return cluster efficient scores for beta."""
    jD=cols.index('D'); Xg=np.delete(X,jD,axis=1)
    off=np.log(df.emp.values)+b0*X[:,jD]
    r=sm.GLM(df[y].values,Xg,family=sm.families.Poisson(),offset=off).fit()
    mu=r.mu; res=df[y].values-mu
    H=(X*mu[:,None]).T@X
    jo=[k for k in range(X.shape[1]) if k!=jD]
    proj=H[jD,jo]@np.linalg.pinv(H[np.ix_(jo,jo)])
    g=pd.factorize(df.industry)[0]; G=g.max()+1
    s=np.zeros(G)
    for k in range(G):
        idx=g==k; Sg=X[idx].T@res[idx]; s[k]=Sg[jD]-proj@Sg[jo]
    return s

def wild_p(df,y,b0,X,cols,W):
    s=score_stat(df,y,b0,X,cols)
    T=s.sum()/np.sqrt((s**2).sum())
    Ts=(W*s).sum(1)/np.sqrt(((W*s)**2).sum(1))
    return np.mean(np.abs(Ts)>=abs(T)-1e-12)

def invert(pfun,bhat,se,alpha=.05):
    grid=np.linspace(bhat-6*se,bhat+6*se,241)
    ps=np.array([pfun(b) for b in grid]); acc=grid[ps>alpha]
    if len(acc)==0: return np.nan,np.nan,ps,grid
    return acc.min(),acc.max(),ps,grid

def ri_p(df,y,b0,inds):
    """Randomization inference: impose H0 beta=b0 via offset, compare |b_obs| with all 28 assignments."""
    df=df.copy(); df['off']=np.log(df.emp)-b0*df.tr*df.post
    def b_for(trset):
        t=df.industry.isin(trset).astype(int)
        z=df.assign(tt=t*df.post)
        m=smf.glm(f'{y} ~ C(industry)+C(fy)+tt',data=z,family=sm.families.Poisson(),offset=z['off']).fit()
        return m.params['tt']
    actual=set(df.loc[df.tr==1,'industry'].unique())
    k=len(actual) if len(actual)<=2 else len(inds)-len(actual)
    assigns=[]
    for c in itertools.combinations(inds,2):
        assigns.append(set(c) if len(actual)==2 else set(inds)-set(c))
    bobs=b_for(actual); bs=np.array([b_for(a) for a in assigns])
    return np.mean(np.abs(bs)>=abs(bobs)-1e-12)

def collapsed(df,y):
    c=df.groupby(['industry','post','tr'],as_index=False).agg(yy=(y,'sum'),emp=('emp','sum'))
    m=smf.glm('yy ~ C(industry)+C(post)+tr:post',data=c,family=sm.families.Poisson(),offset=np.log(c.emp)).fit(cov_type='HC1')
    return np.exp(m.params['tr:post']),*np.exp(m.conf_int().loc['tr:post']),m.pvalues['tr:post']

fmt=lambda e,l,h: f'{e:.2f} ({l:.2f} to {h:.2f})'
fp=lambda p: '<0.001' if p<0.001 else f'{p:.3f}' if p<0.01 else f'{p:.2f}'
rows=[]; summ={}
W8=rng.choice(WEBB,size=(B,8))
for exp in (1,2):
    for y,lab in [('approvals','Approvals'),('claims','Claims'),('cvd_approvals','CVD approvals'),('cvd_claims','CVD claims')]:
        df=setup(exp,y); inds=sorted(df.industry.unique())
        r=fit_glm(df,y); b=r.params['tr:post']; se=r.bse['tr:post']
        con=f'Experiment {exp}'
        rows.append([con,lab,'Main: HC1 robust SE (as in table 2)',fmt(np.exp(b),*np.exp(r.conf_int().loc['tr:post'])),fp(r.pvalues['tr:post'])])
        rc=fit_glm(df,y,'cluster'); sec=rc.bse['tr:post']; G=len(inds); tcrit=stats.t.ppf(.975,G-1)
        pc=2*stats.t.sf(abs(b/sec),G-1)
        rows.append([con,lab,f'SE clustered by industry, t({G-1})',fmt(np.exp(b),np.exp(b-tcrit*sec),np.exp(b+tcrit*sec)),fp(pc)])
        X,cols=design(df,'tr'); W=W8[:,:G]
        pw=wild_p(df,y,0.0,X,cols,W)
        lo,hi,_,_=invert(lambda b0: wild_p(df,y,b0,X,cols,W),b,max(se,sec))
        rows.append([con,lab,'Wild cluster score bootstrap (Webb weights, 9999 draws)',fmt(np.exp(b),np.exp(lo),np.exp(hi)),fp(pw)])
        pr=ri_p(df,y,0.0,inds)
        lo2,hi2,_,_=invert(lambda b0: ri_p(df,y,b0,inds),b,max(se,sec)) if y=='approvals' else (np.nan,np.nan,None,None)
        rows.append([con,lab,'Placebo permutation (28 assignments)',fmt(np.exp(b),np.exp(lo2),np.exp(hi2)) if not np.isnan(lo2) else f'{np.exp(b):.2f} (CI not computed)',fp(pr)])
        e,l,h,p=collapsed(df,y)
        rows.append([con,lab,'Collapsed to one pre and one post period',fmt(e,l,h),fp(p)])
        summ[(exp,y)]=dict(pw=pw,pr=pr,hc1=np.exp(r.conf_int().loc['tr:post']).tolist(),clu=[np.exp(b-tcrit*sec),np.exp(b+tcrit*sec)],wild=[np.exp(lo),np.exp(hi)],ri=[np.exp(lo2),np.exp(hi2)] if not np.isnan(lo2) else None,coll=[l,h])
        print(exp,y,summ[(exp,y)],'p wild',pw,'p ri',pr,flush=True)
# wild cluster bootstrap for approvals excluding FY2023
for exp in (1,2):
    df=setup(exp,'approvals'); df=df[df.fy!=2023].reset_index(drop=True); inds=sorted(df.industry.unique())
    r=fit_glm(df,'approvals'); b=r.params['tr:post']; se=r.bse['tr:post']
    X,cols=design(df,'tr'); W=W8[:,:len(inds)]
    pw=wild_p(df,'approvals',0.0,X,cols,W); lo,hi,_,_=invert(lambda b0: wild_p(df,'approvals',b0,X,cols,W),b,se*2)
    rows.append([f'Experiment {exp}','Approvals','Excluding FY2023, wild cluster score bootstrap',fmt(np.exp(b),np.exp(lo),np.exp(hi)),fp(pw)])
    summ[(exp,'approvals_x23')]=dict(wild=[np.exp(lo),np.exp(hi)],p=pw); print(exp,'x23',np.exp(lo),np.exp(hi),pw,flush=True)
# customer-harassment-prone controls excluded
for exp in (1,2):
    df=setup(exp,'approvals'); df=df[~df.industry.isin(['卸売小売業','宿泊飲食'])]
    r=fit_glm(df,'approvals')
    rows.append([f'Experiment {exp}','Approvals','Excluding wholesale and retail, and accommodation and food services (customer harassment)',fmt(*np.exp([r.params['tr:post'],*r.conf_int().loc['tr:post']])),fp(r.pvalues['tr:post'])])
T=pd.DataFrame(rows,columns=['Contrast','Outcome','Inference / specification','IRR (95% CI)','p'])
T.to_csv(S+'TableS3b_inference.csv',index=False); print(T.to_string())
pd.to_pickle(summ,O+'inference_summary.pkl')
