# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='Noto Sans CJK JP'; plt.rcParams['font.size']=12
D='data/'; O='output/intermediate/'
# ===== 候補1: 出来事別 =====
e=pd.read_csv(D+'rosai_mental_by_event.csv'); pv=e.pivot(index='event',columns='fy',values='approvals')
har=['パワハラ（上司等）','同僚等からのいじめ・暴行','セクハラ','カスハラ（2023.9新設）']; hours=['月80時間以上の時間外労働','2週間以上の連続勤務']
tot=pv.loc['合計']; H=pv.loc[har].sum(); W=pv.loc['仕事内容・仕事量の大きな変化']; L=pv.loc[hours].sum(); A=pv.loc[['悲惨な事故・災害の体験','重度の病気やケガ']].sum()
oth=tot-H-W-L-A-pv.loc['特別な出来事（極度の負荷等）']
T=pd.DataFrame({'合計':tot,'ハラスメント計':H,'　うちパワハラ':pv.loc['パワハラ（上司等）'],'　うちカスハラ':pv.loc['カスハラ（2023.9新設）'],'　うちセクハラ':pv.loc['セクハラ'],'仕事量の変化':W,'長時間労働・連続勤務':L,'事故・災害・傷病':A,'特別な出来事':pv.loc['特別な出来事（極度の負荷等）'],'その他':oth}).T
share=(T/tot*100).round(1)
contrib=pd.DataFrame({'2022→2023 増分':T[2023]-T[2022],'2023→2024 増分':T[2024]-T[2023],'2022→2024 増分':T[2024]-T[2022]})
contrib['2022→2024 寄与%']=(contrib['2022→2024 増分']/contrib.loc['合計','2022→2024 増分']*100).round(1)
T.to_csv(O+'t17_events_approvals.csv'); share.to_csv(O+'t18_events_share.csv'); contrib.to_csv(O+'t19_events_contrib.csv')
print(T); print(share); print(contrib)
fig,ax=plt.subplots(1,2,figsize=(13,5))
cats=['ハラスメント計','仕事量の変化','長時間労働・連続勤務','事故・災害・傷病','特別な出来事','その他']
bottom=np.zeros(len(tot.index))
for c in cats: ax[0].bar(tot.index,T.loc[c],bottom=bottom,label=c); bottom+=T.loc[c].values
ax[0].axvline(2023.5,ls='--',color='orange'); ax[0].text(2023.55,ax[0].get_ylim()[1]*0.93,'認定基準改正\n2023.9',fontsize=9,color='darkorange'); ax[0].set_title('精神障害 支給決定件数の出来事別内訳'); ax[0].legend(fontsize=8); ax[0].set_xlabel('年度')
for c in ['パワハラ（上司等）','カスハラ（2023.9新設）','セクハラ','同僚等からのいじめ・暴行']: ax[1].plot(pv.columns,pv.loc[c],marker='o',label=c)
ax[1].plot(pv.columns,L,marker='s',ls='--',label='長時間労働・連続勤務'); ax[1].set_title('ハラスメント系 vs 労働時間系（支給決定件数）'); ax[1].legend(fontsize=8); ax[1].set_xlabel('年度')
plt.tight_layout(); plt.savefig(O+'fig12_events.png',dpi=160); plt.close()

# ===== 候補3: 疾患×年齢 =====
k=pd.read_csv(D+'kanja_disease_by_age.csv'); P=pd.read_csv(D+'population_by_age.csv').set_index('year')
amap={'0-19':'age_0_19','20-29':'age_20_29','30-39':'age_30_39','40-49':'age_40_49','50-59':'age_50_59','60-69':'age_60_69','70+':'age_70p'}
dis=['F計','気分障害','神経症性','統合失調症','その他F（認知症・発達障害・物質等）']
k['pop_k']=[P.loc[y,amap[a]] for y,a in zip(k.year,k.age10)]
for d in dis: k[d+'_rate']=k[d]/k.pop_k*1e5   # 人口10万対（千人/千人）
rate=k.set_index(['year','age10'])[[d+'_rate' for d in dis]].round(0)
rate.to_csv(O+'t20_disease_age_rates.csv')
# 2008→2017 の年齢別率の増加（10万対）を疾患別に分解
r08=k[k.year==2008].set_index('age10'); r17=k[k.year==2017].set_index('age10'); r23=k[k.year==2023].set_index('age10')
dec=pd.DataFrame({d:(r17[d+'_rate']-r08[d+'_rate']).round(0) for d in dis}); dec['F計増加に占める気分+神経症%']=((dec['気分障害']+dec['神経症性'])/dec['F計']*100).round(0)
dec['F計増加に占めるその他F%']=(dec['その他F（認知症・発達障害・物質等）']/dec['F計']*100).round(0)
dec.to_csv(O+'t21_disease_age_decomp_2008_2017.csv'); print(rate.loc[[2008,2017,2023]]); print(dec)
# 2017→2023（推計変更をまたぐ：参考）
dec2=pd.DataFrame({d:(r23[d+'_rate']/r17[d+'_rate']).round(2) for d in dis}); dec2.to_csv(O+'t22_disease_age_ratio_2017_2023.csv'); print(dec2)
fig,ax=plt.subplots(1,3,figsize=(16,5)); order=['0-19','20-29','30-39','40-49','50-59','60-69','70+']
for i,d in enumerate(['気分障害','神経症性','その他F（認知症・発達障害・物質等）']):
    for y in [2008,2011,2014,2017]: ax[i].plot(order,[k[(k.year==y)&(k.age10==a)][d+'_rate'].iloc[0] for a in order],marker='o',label=str(y))
    ax[i].plot(order,[k[(k.year==2023)&(k.age10==a)][d+'_rate'].iloc[0] for a in order],marker='s',ls='--',color='k',label='2023（新推計）')
    ax[i].set_title(d+'（人口10万対）'); ax[i].legend(fontsize=8); ax[i].set_xlabel('年齢')
plt.tight_layout(); plt.savefig(O+'fig13_disease_age_rates.png',dpi=160); plt.close()
