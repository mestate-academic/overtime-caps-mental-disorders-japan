# -*- coding: utf-8 -*-
import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='Noto Sans CJK JP'; plt.rcParams['font.size']=12
D='data/'; O='output/intermediate/'
df=pd.read_csv(D+'rosai_mental_by_industry.csv'); cvd=pd.read_csv(D+'rosai_cvd_by_industry.csv'); emp=pd.read_csv(D+'employment_by_industry.csv')
m={'製造業':'製造業','建設業':'建設業','運輸業郵便業':'運輸業郵便業','卸売小売業':'卸売小売業','金融保険業':'金融保険業','教育学習支援業':'教育学習支援業','医療福祉':'医療福祉','情報通信業':'情報通信業','宿泊飲食':'宿泊飲食'}
el=emp.melt(id_vars='year',var_name='industry',value_name='emp_man'); el=el[el.industry.isin(m.values())]; el['fy']=el.year
d=df[df.industry.isin(m.keys())].merge(el[['fy','industry','emp_man']],on=['fy','industry'],how='left').merge(cvd,on=['fy','industry'],how='left')
d=d[d.fy>=2011].copy(); d['emp']=d.emp_man*1e4
d['late']=d.industry.isin(['建設業','運輸業郵便業']).astype(int); d['med']=(d.industry=='医療福祉').astype(int)
d['rate']=d.approvals/d.emp*1e6; d['crate']=d.claims/d.emp*1e6
d.to_csv(O+'t6_industry_rates.csv',index=False)

# 図5: 率（100万就業者あたり）
grp=d.assign(group=np.where(d.late==1,'猶予業種(建設・運輸)',np.where(d.med==1,'医療福祉','一般業種(6業種)')))
g=grp.groupby(['group','fy']).agg(approvals=('approvals','sum'),claims=('claims','sum'),emp=('emp','sum')).reset_index()
g['rate']=g.approvals/g.emp*1e6; g['crate']=g.claims/g.emp*1e6
fig,ax=plt.subplots(1,2,figsize=(13,5))
for k,s in g.groupby('group'): ax[0].plot(s.fy,s.rate,marker='o',label=k); ax[1].plot(s[s.fy>=2018].fy,s[s.fy>=2018].crate,marker='o',label=k)
ax[0].set_title('精神障害 労災支給決定率（就業者100万人あたり）'); ax[1].set_title('精神障害 労災請求率（就業者100万人あたり, FY2018-）')
for a in ax: a.axvline(2019,ls='--',color='k',lw=.8); a.axvline(2024,ls='--',color='r',lw=.8); a.legend(fontsize=9); a.set_xlabel('年度')
plt.tight_layout(); plt.savefig(O+'fig5_rates_by_group.png',dpi=160); plt.close()
g.to_csv(O+'t7_group_rates.csv',index=False)

# Event study with offset (医療福祉除外), ref 2023
dd=d[d.med==0].copy(); years=sorted(dd.fy.unique()); ref=2023
for y in years:
    if y!=ref: dd[f'ev_{y}']=((dd.fy==y)&(dd.late==1)).astype(int)
form='approvals ~ C(industry)+C(fy)+'+'+'.join([f'ev_{y}' for y in years if y!=ref])
mo=smf.glm(form,data=dd,family=sm.families.Poisson(),offset=np.log(dd.emp)).fit(cov_type='HC1')
es=pd.DataFrame({'fy':[y for y in years if y!=ref],'coef':[mo.params[f'ev_{y}'] for y in years if y!=ref],'se':[mo.bse[f'ev_{y}'] for y in years if y!=ref]})
es=pd.concat([es,pd.DataFrame({'fy':[ref],'coef':[0.0],'se':[0.0]})]).sort_values('fy'); es['IRR']=np.exp(es.coef); es['lo']=np.exp(es.coef-1.96*es.se); es['hi']=np.exp(es.coef+1.96*es.se)
es.to_csv(O+'t8_event_study_offset.csv',index=False)
# DiD 2024 mental vs CVD (negative control) FY2021-2025 with offset
d2=dd[dd.fy>=2021].copy(); d2['post24']=(d2.fy>=2024).astype(int)
mm=smf.glm('approvals ~ C(industry)+C(fy)+late:post24',data=d2,family=sm.families.Poisson(),offset=np.log(d2.emp)).fit(cov_type='HC1')
mc=smf.glm('cvd_approvals ~ C(industry)+C(fy)+late:post24',data=d2,family=sm.families.Poisson(),offset=np.log(d2.emp)).fit(cov_type='HC1')
mcl=smf.glm('claims ~ C(industry)+C(fy)+late:post24',data=d2,family=sm.families.Poisson(),offset=np.log(d2.emp)).fit(cov_type='HC1')
mcc=smf.glm('cvd_claims ~ C(industry)+C(fy)+late:post24',data=d2,family=sm.families.Poisson(),offset=np.log(d2.emp)).fit(cov_type='HC1')
# DiD 2019 (general industries treated) FY2016-2023
d3=dd[(dd.fy>=2016)&(dd.fy<=2023)].copy(); d3['post19']=(d3.fy>=2019).astype(int); d3['general']=1-d3.late
m19=smf.glm('approvals ~ C(industry)+C(fy)+general:post19',data=d3,family=sm.families.Poisson(),offset=np.log(d3.emp)).fit(cov_type='HC1')
def irr(mod,k): return '%.2f (%.2f-%.2f), p=%.3f'%(np.exp(mod.params[k]),*np.exp(mod.conf_int().loc[k]),mod.pvalues[k])
res=pd.DataFrame([
 ['2019/20規制','精神障害 支給決定（就業者率）','一般業種×2019以降',irr(m19,'general:post19')],
 ['2024規制','精神障害 支給決定（就業者率）','猶予業種×2024以降',irr(mm,'late:post24')],
 ['2024規制','精神障害 請求（就業者率）','猶予業種×2024以降',irr(mcl,'late:post24')],
 ['2024規制','脳・心臓疾患 支給決定（陰性対照）','猶予業種×2024以降',irr(mc,'late:post24')],
 ['2024規制','脳・心臓疾患 請求（陰性対照）','猶予業種×2024以降',irr(mcc,'late:post24')]],columns=['イベント','アウトカム','項','IRR (95%CI)'])
res.to_csv(O+'t9_did_with_offset_and_control.csv',index=False)
fig,ax=plt.subplots(figsize=(9,5))
ax.errorbar(es.fy,es.IRR,yerr=[es.IRR-es.lo,es.hi-es.IRR],fmt='o',capsize=3,color='navy'); ax.axhline(1,color='gray'); ax.axvline(2019,ls='--',color='k',lw=.8); ax.axvline(2024,ls='--',color='r',lw=.8); ax.set_yscale('log')
ax.set_ylabel('IRR（猶予業種 vs 一般6業種、2023年度基準）'); ax.set_xlabel('年度'); ax.set_title('Event study（就業者数オフセット付きPoisson, 業種FE+年度FE）')
plt.tight_layout(); plt.savefig(O+'fig6_event_study_offset.png',dpi=160); plt.close()
# 脳心 vs 精神 group trend FY2021-25
gc=d2.assign(group=np.where(d2.late==1,'猶予業種','一般業種')).groupby(['group','fy']).agg(m=('approvals','sum'),c=('cvd_approvals','sum'),e=('emp','sum')).reset_index()
fig,ax=plt.subplots(1,2,figsize=(12,4.5))
for k,s in gc.groupby('group'): ax[0].plot(s.fy,s.m/s.e*1e6,marker='o',label=k); ax[1].plot(s.fy,s.c/s.e*1e6,marker='o',label=k)
ax[0].set_title('精神障害 支給決定率（/100万就業者）'); ax[1].set_title('脳・心臓疾患 支給決定率（陰性対照）')
for a in ax: a.axvline(2024,ls='--',color='r',lw=.8); a.legend(); a.set_xlabel('年度')
plt.tight_layout(); plt.savefig(O+'fig7_mental_vs_cvd.png',dpi=160); plt.close()

# ===== 候補3: 労災 年齢別 =====
ag=pd.read_csv(D+'rosai_mental_by_age.csv'); pv=ag.pivot(index='fy',columns='age',values='approvals')
order=['19歳以下','20-29','30-39','40-49','50-59','60+']; pv=pv[order]
sh=pv.div(pv.sum(axis=1),axis=0)*100; idx=pv/pv.loc[2011]*100
pd.concat({'approvals':pv,'share_%':sh.round(1),'index_2011':idx.round(0)},axis=1).to_csv(O+'t10_rosai_by_age.csv')
fig,ax=plt.subplots(1,2,figsize=(13,5))
for c in order[1:]: ax[0].plot(pv.index,pv[c],marker='o',label=c)
ax[0].set_title('精神障害 労災支給決定件数（年齢階級別）'); ax[0].legend(fontsize=9); ax[0].set_xlabel('年度')
pc=pd.read_csv(D+'kanja_chosa_mental.csv')
w=pv[['20-29','30-39','40-49','50-59']].sum(axis=1); o=pv['60+']
ax[1].plot(pv.index,w/w.loc[2011]*100,marker='o',label='労災認定 20-59歳（2011=100）'); ax[1].plot(pv.index,o/o.loc[2011]*100,marker='o',label='労災認定 60歳以上（2011=100）')
kw=pc[['age_20_29','age_30_39','age_40_49','age_50_59']].sum(axis=1); kw=pd.Series(kw.values,index=pc.year); k70=pd.Series(pc.age_70p.values,index=pc.year)
old=[y for y in kw.index if y<=2017]
ax[1].plot(old,kw.loc[old]/kw.loc[2011]*100,marker='s',ls='--',label='患者調査 20-59歳（2011=100, 旧推計）'); ax[1].plot(old,k70.loc[old]/k70.loc[2011]*100,marker='s',ls='--',label='患者調査 70歳以上（2011=100, 旧推計）')
ax[1].set_title('就労年齢層：労災認定 vs 患者数（指数）'); ax[1].legend(fontsize=8); ax[1].set_xlabel('年（度）')
plt.tight_layout(); plt.savefig(O+'fig8_age_rosai_vs_kanja.png',dpi=160); plt.close()
print(res.to_string()); print(es[['fy','IRR','lo','hi']].round(2).to_string()); print(g.pivot(index='fy',columns='group',values='rate').round(1)); print(sh.round(1))
