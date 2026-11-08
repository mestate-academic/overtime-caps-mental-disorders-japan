# -*- coding: utf-8 -*-
import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='Noto Sans CJK JP'; plt.rcParams['font.size']=12
D='data/'; O='output/intermediate/'

# ===== 候補1: 都道府県パネル（曝露強度DiD） =====
p=pd.read_csv(D+'rosai_mental_by_pref.csv'); c=pd.read_csv(D+'census2015_pref_industry.csv')
d=p.merge(c,on='pref'); d['exp_late']=(d.emp_const+d.emp_transport)/d.emp_total*100   # 猶予業種就業者割合(%)
d['exp_med']=d.emp_medwel/d.emp_total*100; d['post24']=(d.fy>=2024).astype(int); d['y23']=(d.fy==2023).astype(int)
d['exp_z']=(d.exp_late-d.exp_late.mean())/d.exp_late.std()
d['rate']=d.approvals/d.emp_total*1e6; d['crate']=d.claims/d.emp_total*1e6
d.to_csv(O+'t12_pref_panel.csv',index=False)
# 記述：曝露上位/下位四分位
q=d[d.fy==2021].exp_late.quantile([.25,.75]); d['expq']=np.where(d.exp_late>=q[.75],'高曝露(上位25%)',np.where(d.exp_late<=q[.25],'低曝露(下位25%)','中'))
g=d.groupby(['expq','fy']).agg(a=('approvals','sum'),cl=('claims','sum'),e=('emp_total','sum')).reset_index(); g['rate']=g.a/g.e*1e6; g['crate']=g.cl/g.e*1e6
g.to_csv(O+'t13_pref_exposure_groups.csv',index=False)
# Poisson: pref FE + year FE + exp_z×post24 (+ exp_z×2023), offset log emp, cluster by pref
def fit(y,extra=''):
    m=smf.glm(f'{y} ~ C(pref)+C(fy)+exp_z:post24'+extra,data=d,family=sm.families.Poisson(),offset=np.log(d.emp_total)).fit(cov_type='cluster',cov_kwds={'groups':d.pref})
    return m
res=[]
for y in ['approvals','claims']:
    m=fit(y); res.append([y,'exp_z×post2024（1SD曝露増あたり）','%.3f (%.3f-%.3f) p=%.3f'%(np.exp(m.params['exp_z:post24']),*np.exp(m.conf_int().loc['exp_z:post24']),m.pvalues['exp_z:post24'])])
    m2=fit(y,'+exp_z:y23'); res.append([y,'exp_z×FY2023（先行）','%.3f (%.3f-%.3f) p=%.3f'%(np.exp(m2.params['exp_z:y23']),*np.exp(m2.conf_int().loc['exp_z:y23']),m2.pvalues['exp_z:y23'])])
    res.append([y,'exp_z×post2024（FY2023先行項を含むモデル）','%.3f (%.3f-%.3f) p=%.3f'%(np.exp(m2.params['exp_z:post24']),*np.exp(m2.conf_int().loc['exp_z:post24']),m2.pvalues['exp_z:post24'])])
# event study by year
for y in ['approvals','claims']:
    dd=d.copy()
    for fy in [2022,2023,2024,2025]: dd[f'e{fy}']=dd.exp_z*(dd.fy==fy)
    m=smf.glm(f'{y} ~ C(pref)+C(fy)+e2022+e2023+e2024+e2025',data=dd,family=sm.families.Poisson(),offset=np.log(dd.emp_total)).fit(cov_type='cluster',cov_kwds={'groups':dd.pref})
    for fy in [2022,2023,2024,2025]: res.append([y,f'event study exp_z×FY{fy}（基準FY2021）','%.3f (%.3f-%.3f) p=%.3f'%(np.exp(m.params[f'e{fy}']),*np.exp(m.conf_int().loc[f'e{fy}']),m.pvalues[f'e{fy}'])])
R=pd.DataFrame(res,columns=['アウトカム','項','IRR (95%CI)']); R.to_csv(O+'t14_pref_did.csv',index=False); print(R.to_string())
fig,ax=plt.subplots(1,2,figsize=(12,4.5))
for k,s in g[g.expq!='中'].groupby('expq'): ax[0].plot(s.fy,s.rate,marker='o',label=k); ax[1].plot(s.fy,s.crate,marker='o',label=k)
ax[0].set_title('都道府県群別 支給決定率（/100万就業者, 2015）'); ax[1].set_title('同 請求率')
for a in ax: a.axvline(2024,ls='--',color='r',lw=.8); a.legend(fontsize=9); a.set_xlabel('年度')
plt.tight_layout(); plt.savefig(O+'fig9_pref_exposure.png',dpi=160); plt.close()
# 散布図：曝露 vs 2021-23→2024-25 の変化率
pre=d[d.fy<=2023].groupby('pref').approvals.sum()/3; post=d[d.fy>=2024].groupby('pref').approvals.sum()/2
ch=pd.DataFrame({'exp':d.groupby('pref').exp_late.first(),'ratio':post/pre,'pre':pre})
fig,ax=plt.subplots(figsize=(7,5)); ax.scatter(ch.exp,np.log(ch.ratio),s=ch.pre*2+10,alpha=.6)
for n,r in ch.iterrows():
    if r.pre>30: ax.annotate(n,(r.exp,np.log(r.ratio)),fontsize=8)
ax.axhline(0,color='gray'); ax.set_xlabel('猶予業種（建設＋運輸）就業者割合 %（2015年国勢調査）'); ax.set_ylabel('log(FY24-25平均 / FY21-23平均) 支給決定')
ax.set_title('都道府県別：猶予業種曝露と2024年以降の変化'); plt.tight_layout(); plt.savefig(O+'fig10_pref_scatter.png',dpi=160); plt.close()

# ===== 候補3: 年齢調整率 =====
pc=pd.read_csv(D+'kanja_chosa_mental.csv'); P=pd.read_csv(D+'population_by_age.csv').set_index('year')
ages=['age_0_19','age_20_29','age_30_39','age_40_49','age_50_59','age_60_69','age_70p']; lab={'age_0_19':'0-19','age_20_29':'20-29','age_30_39':'30-39','age_40_49':'40-49','age_50_59':'50-59','age_60_69':'60-69','age_70p':'70+'}
pc=pc.set_index('year'); rate=pd.DataFrame({a:pc[a]*1e4/(P.loc[pc.index,a]*1e3)*1e5 for a in ages})  # 人口10万対
std=P.loc[2015]; w=std/std.sum()
asr=(rate*w).sum(axis=1); crude=pc.total*1e4/(P.loc[pc.index,ages].sum(axis=1)*1e3)*1e5
out=rate.rename(columns=lab).round(0); out['粗率']=crude.round(0); out['年齢調整率(2015年人口基準)']=asr.round(0); out.to_csv(O+'t15_age_specific_rates.csv'); print(out)
# 分解 2002→2017: Δ総数 = 人口規模・構造の変化分 + 年齢別率の変化分（Kitagawa）
def kitagawa(y0,y1):
    N0=P.loc[y0,ages]*1e3; N1=P.loc[y1,ages]*1e3; r0=rate.loc[y0]/1e5; r1=rate.loc[y1]/1e5
    pop_eff=((N1-N0)*(r0+r1)/2).sum(); rate_eff=((r1-r0)*(N0+N1)/2).sum()
    return pop_eff/1e4, rate_eff/1e4, (pop_eff+rate_eff)/1e4
k1=kitagawa(2002,2017); k2=kitagawa(2020,2023)
K=pd.DataFrame([['2002→2017',*[round(x,1) for x in k1]],['2020→2023',*[round(x,1) for x in k2]]],columns=['期間','人口（高齢化・規模）要因 万人','年齢別受療率の変化要因 万人','合計変化 万人'])
K.to_csv(O+'t16_kitagawa.csv',index=False); print(K)
# 年齢別率の変化（図）
fig,ax=plt.subplots(1,2,figsize=(13,5))
old=[2002,2005,2008,2011,2014,2017]
for a in ages: ax[0].plot(old,rate.loc[old,a],marker='o',label=lab[a])
ax[0].set_title('精神疾患 総患者数の年齢別率（人口10万対, 旧推計 2002-2017）'); ax[0].legend(fontsize=8,ncol=2); ax[0].set_xlabel('年')
ax[1].plot(old,crude.loc[old],marker='o',label='粗率'); ax[1].plot(old,asr.loc[old],marker='s',label='年齢調整率（2015年人口基準）')
ax[1].plot([2020,2023],crude.loc[[2020,2023]],marker='o',ls='--',color='C0'); ax[1].plot([2020,2023],asr.loc[[2020,2023]],marker='s',ls='--',color='C1')
ax[1].set_title('粗率 vs 年齢調整率（人口10万対）'); ax[1].legend(); ax[1].set_xlabel('年')
plt.tight_layout(); plt.savefig(O+'fig11_age_adjusted.png',dpi=160); plt.close()
