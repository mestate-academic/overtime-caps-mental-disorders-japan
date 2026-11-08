# -*- coding: utf-8 -*-
"""English-labelled figures for OEM submission + supplementary tables S1-S4"""
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.lines
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
D='data/'; O='output/intermediate/'; S='output/tables/'
import os; os.makedirs(S,exist_ok=True)
COL={'Non-exempted (6 industries)':'#1f4e79','Exempted (construction, transport)':'#c55a11','Health care and welfare':'#7f7f7f'}
gmap={'一般業種(6業種)':'Non-exempted (6 industries)','猶予業種(建設・運輸)':'Exempted (construction, transport)','医療福祉':'Health care and welfare'}

# ---------- shared design elements ----------
CT='#c55a11'; CC='#1f4e79'; CH='#8c8c8c'
LAB={'Exempted (construction, transport)':'Construction & transport\n(capped Apr 2024)','Non-exempted (6 industries)':'6 comparison industries\n(capped Apr 2019/2020)','Health care and welfare':'Health care & welfare\n(physicians Apr 2024,\nothers Apr 2019/2020)'}
COL2={'Exempted (construction, transport)':CT,'Non-exempted (6 industries)':CC,'Health care and welfare':CH}
BANDS=[(2015.5,2018.5,'#f2f2f2','No cap'),(2018.5,2023.5,'#e3ecf5','6 industries capped\n(large firms Apr 2019,\nsmall & medium-sized\nfirms Apr 2020)'),(2023.5,2025.5,'#fbe5d6','All capped\n(construction\n& transport\nApr 2024)')]
def bands(a,top=True,xmin=2015.5,xmax=2025.5):
    for x0,x1,c,t in BANDS:
        x0,x1=max(x0,xmin),min(x1,xmax)
        if x1<=x0: continue
        a.axvspan(x0,x1,color=c,zorder=0,lw=0)
        if top: a.text((x0+x1)/2,1.01,t,transform=a.get_xaxis_transform(),ha='center',va='bottom',fontsize=7.5,fontweight='bold',color='#404040',linespacing=1.1)
    if xmin<2019.5<xmax: a.axvline(2019.5,color='#7f9fbf',ls=':',lw=0.9,zorder=0.5)  # April 2020: SMEs capped
    yrs=range(int(xmin+0.5),int(xmax+0.5))
    a.set_xlim(xmin,xmax); a.set_xticks(list(yrs)); a.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    a.set_xlabel('Fiscal year (April–March)')
def exp_brackets(a,y):
    for x0,x1,t,c in [(2016,2023,'Experiment 1 (2019–20 cap)',CC),(2021,2025,'Experiment 2 (2024 cap)',CT)]:
        pass

# ---------- Figure 1: 10-year trends with the two experiments ----------
g=pd.read_csv(O+'t7_group_rates.csv'); g=g[g.fy>=2016]; g['grp']=g.group.map(gmap)
fig,ax=plt.subplots(1,2,figsize=(12,4.8))
for i,(col,title) in enumerate([('rate','A  Approved claims'),('crate','B  Claims filed')]):
    a=ax[i]; bands(a)
    for k in ['Health care and welfare','Exempted (construction, transport)','Non-exempted (6 industries)']:
        s=g[g.grp==k]; ls='--' if k.startswith('Health') else '-'
        a.plot(s.fy,s[col],marker='o',ms=4,lw=2,ls=ls,color=COL2[k])
        a.annotate(LAB[k],(s.fy.iloc[-1],s[col].iloc[-1]),xytext=(6,-12 if k.startswith('Health') else 0),textcoords='offset points',va='center',fontsize=7.5,color=COL2[k],fontweight='bold',annotation_clip=False)
    a.set_title(title,loc='left',fontweight='bold',pad=52); a.set_ylabel('Per million employed persons')
    a.set_ylim(bottom=0)
plt.tight_layout(w_pad=9); plt.subplots_adjust(right=0.87); plt.savefig('output/figures/Figure1.png',dpi=300); plt.close()

# ---------- Figure 2: one event study per natural experiment (reference = mean of own pre-cap period) ----------
R=pd.read_csv(O+'t25_es_pooled.csv')
fig,ax=plt.subplots(1,2,figsize=(10.5,4.8),sharey=True,gridspec_kw={'width_ratios':[8,6]})
spec=[(1,CC,'A  Experiment 1: April 2019/2020 cap\n     6 industries (newly capped) vs\n     construction & transport (control)',(2015.6,2018.4),'Reference = mean of\nFY2016–18 (set to 1)'),
      (2,CT,'B  Experiment 2: April 2024 cap\n     Construction & transport (newly capped)\n     vs 6 industries (control)',(2020.6,2023.4),'Reference = mean of\nFY2021–23 (set to 1)')]
for a,(k,c,title,(r0,r1),rlab),(xa,xb) in zip(ax,spec,[(2015.5,2023.5),(2019.5,2025.5)]):
    bands(a,xmin=xa,xmax=xb)
    a.axhline(1,color='k',lw=0.8)
    for out,dx,mk,fc,lab in [('approvals',-0.13,'o',c,'Mental disorders (main outcome)'),('cvd_approvals',0.13,'s','white','Cerebro-cardiovascular disease (positive control for exposure)')]:
        q=R[(R.exp==k)&(R.outcome==out)]
        col=c if out=='approvals' else '#7f7f7f'
        a.errorbar(q.fy+dx,q.IRR,yerr=[q.IRR-q.lo,q.hi-q.IRR],fmt=mk,ms=5,mfc=fc,mec=col,capsize=2.5,lw=1.4,color=col,label=lab)
    a.plot([r0,r1],[0.47,0.47],color='#333333',lw=2.5,solid_capstyle='butt')
    a.text((r0+r1)/2,0.49,rlab,ha='center',va='bottom',fontsize=7.5,color='#333333')
    a.set_yscale('log'); a.set_ylim(0.44,2.0); a.set_yticks([0.5,0.7,1,1.4,2]); a.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter()); a.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    a.set_title(title,loc='left',fontweight='bold',pad=52,fontsize=9.5)
ax[0].set_ylabel('IRR relative to the pre-cap mean (= 1)\n<1 = decline in newly capped group')
L2=matplotlib.lines.Line2D
hl=[L2([],[],marker='o',ls='',color=CC,ms=5),L2([],[],marker='o',ls='',color=CT,ms=5),L2([],[],marker='s',ls='',mfc='white',mec='#7f7f7f',ms=5),L2([],[],color='#7f9fbf',ls=':')]
ll=['Mental disorders (main outcome), experiment 1','Mental disorders (main outcome), experiment 2','Cerebro-cardiovascular disease (positive control for exposure)','April 2020: cap extended to small and medium-sized firms']
fig.legend(hl,ll,loc='lower center',ncol=2,frameon=False,fontsize=8.5)
plt.tight_layout(w_pad=2,rect=(0,0.09,1,1)); plt.savefig('output/figures/Figure2.png',dpi=300); plt.close()

# ---------- Supplementary Figure S1 (prefecture scatter) ----------
p=pd.read_csv(O+'t12_pref_panel.csv')
pre=p[p.fy<=2023].groupby('pref').approvals.sum()/3; post=p[p.fy>=2024].groupby('pref').approvals.sum()/2
ch=pd.DataFrame({'exp':p.groupby('pref').exp_late.first(),'ratio':post/pre,'pre':pre})
EN={'東京':'Tokyo','大阪':'Osaka','神奈川':'Kanagawa','愛知':'Aichi','福岡':'Fukuoka','北海道':'Hokkaido','埼玉':'Saitama','千葉':'Chiba','兵庫':'Hyogo','京都':'Kyoto','宮城':'Miyagi','広島':'Hiroshima','静岡':'Shizuoka'}
fig,ax=plt.subplots(figsize=(6.5,4.5)); ax.scatter(ch.exp,np.log(ch.ratio),s=ch.pre*2+12,alpha=.55,color='#1f4e79',edgecolor='white')
for n,r in ch.iterrows():
    if n in EN and r.pre>15: ax.annotate(EN[n],(r.exp,np.log(r.ratio)),fontsize=7,xytext=(3,3),textcoords='offset points')
b=np.polyfit(ch.exp,np.log(ch.ratio),1,w=np.sqrt(ch.pre)); xs=np.linspace(ch.exp.min(),ch.exp.max(),50); ax.plot(xs,b[0]*xs+b[1],color='#c55a11',lw=1)
ax.axhline(0,color='grey',lw=0.8); ax.set_xlabel('Share of employment in construction and transport, % (2015 Census)')
ax.set_ylabel('log ratio of mean annual approvals\n(FY2024–25 vs FY2021–23)')
plt.tight_layout(); plt.savefig('output/figures/FigureS1.png',dpi=300); plt.close()

# ---------- Supplementary Figure S2 (events) ----------
T=pd.read_csv(O+'t17_events_approvals.csv',index_col=0); T.columns=T.columns.astype(int)
cats={'ハラスメント計':'Harassment','仕事量の変化':'Change in workload','長時間労働・連続勤務':'Working hours','事故・災害・傷病':'Accidents, disasters, injury','特別な出来事':'Special events','その他':'Other'}
colors=['#c55a11','#f4b183','#1f4e79','#9dc3e6','#a5a5a5','#d9d9d9']
fig,ax=plt.subplots(figsize=(7,4.5)); bottom=np.zeros(len(T.columns))
for (k,v),c in zip(cats.items(),colors): ax.bar(T.columns,T.loc[k],bottom=bottom,label=v,color=c,edgecolor='white'); bottom+=T.loc[k].values
ax.axvline(2019.5+2/12,color='grey',ls=':',lw=1); ax.axvline(2022.5+5/12,color='k',ls=':',lw=1); ax.set_ylim(0,1300); ax.text(2019.5+2/12,1290,'Power harassment\nadded (May 2020)',fontsize=7,va='top',ha='center'); ax.text(2022.5+5/12,1290,'Criteria revised,\ncustomer harassment\nadded (Sept 2023)',fontsize=7,va='top',ha='center')
ax.legend(fontsize=7.5,frameon=False,loc='upper left',bbox_to_anchor=(0,0.88)); ax.set_xticks(range(2016,2026))
ax.set_xlabel('Fiscal year (April–March)'); ax.set_ylabel('Approved claims (n)')
plt.tight_layout(); plt.savefig('output/figures/FigureS2.png',dpi=300); plt.close()

# ---------- Supplementary tables ----------
# S1: transcription checks
ind=pd.read_csv(D+'rosai_mental_by_industry.csv'); nat=pd.read_csv(D+'rosai_mental_national.csv').set_index('fy')
pref=pd.read_csv(D+'rosai_mental_by_pref.csv'); ev=pd.read_csv(D+'rosai_mental_by_event.csv'); cvd=pd.read_csv(D+'rosai_cvd_by_industry.csv')
rows=[]
for y in range(2016,2026):
    x=ind[(ind.fy==y)&(ind.industry!='合計')]
    r={'FY':y,'Published national approvals':int(nat.loc[y,'approvals']),'Sum of industries (approvals)':int(x.approvals.sum())}
    r['Sum of industries (claims)']=int(x.claims.sum()) if x.claims.notna().all() else '–'
    r['Published national claims']=int(nat.loc[y,'claims']) if y>=2016 else '–'
    px=pref[pref.fy==y]; r['Sum of 47 prefectures (approvals)']=int(px.approvals.sum()) if len(px) else '–'
    cx=cvd[(cvd.fy==y)]; r['CVD claims: sum of industries / published']=(f"{int(cx[cx.industry!='合計'].cvd_claims.sum())} / {int(cx[cx.industry=='合計'].cvd_claims.iloc[0])}") if len(cx) else '–'
    r['CVD approvals: sum of industries / published']=(f"{int(cx[cx.industry!='合計'].cvd_approvals.sum())} / {int(cx[cx.industry=='合計'].cvd_approvals.iloc[0])}") if len(cx) else '–'
    rows.append(r)
S1=pd.DataFrame(rows); S1['Match']=np.where((S1['Published national approvals']==S1['Sum of industries (approvals)'])&((S1['Sum of 47 prefectures (approvals)']=='–')|(S1['Sum of 47 prefectures (approvals)']==S1['Published national approvals'])),'Yes','No')
S1.to_csv(S+'TableS1.csv',index=False)
# S2: prefecture exposure groups
g13=pd.read_csv(O+'t13_pref_exposure_groups.csv'); g13['grp']=g13.expq.map({'高曝露(上位25%)':'High exposure (top quartile)','中':'Middle','低曝露(下位25%)':'Low exposure (bottom quartile)'})
S2=g13.pivot(index='fy',columns='grp',values='rate').round(1)[['Low exposure (bottom quartile)','Middle','High exposure (top quartile)']]
S2c=g13.pivot(index='fy',columns='grp',values='crate').round(1)[['Low exposure (bottom quartile)','Middle','High exposure (top quartile)']]
S2=pd.concat({'Approvals per million':S2,'Claims per million':S2c},axis=1); S2.to_csv(S+'TableS2.csv')
# S3: prefecture event study + DiD
t14=pd.read_csv(O+'t14_pref_did.csv'); tr={'approvals':'Approvals','claims':'Claims'}
def term(s):
    s=s.replace('exp_z×post2024（1SD曝露増あたり）','Exposure (per SD) × post-2024').replace('exp_z×FY2023（先行）','Exposure (per SD) × FY2023 (anticipation)').replace('exp_z×post2024（FY2023先行項を含むモデル）','Exposure × post-2024 (model including FY2023 term)')
    return s.replace('event study exp_z×','Event study: exposure × ').replace('（基準FY2021）',' (ref. FY2021)')
S3=pd.DataFrame({'Outcome':t14['アウトカム'].map(tr),'Term':t14['項'].map(term),'IRR (95% CI)':t14['IRR (95%CI)'].str.replace('-',' to ',regex=False)}); S3.to_csv(S+'TableS3.csv',index=False)
# S4: industry event study full
es=pd.read_csv(O+'t8_event_study_offset.csv'); S4=es[['fy','IRR','lo','hi']].copy(); S4['IRR (95% CI)']=S4.apply(lambda r:'1 (reference)' if r.fy==2023 else f'{r.IRR:.2f} ({r.lo:.2f} to {r.hi:.2f})',axis=1)
S4=S4[['fy','IRR (95% CI)']].rename(columns={'fy':'FY'}); S4.to_csv(S+'TableS4.csv',index=False)
print(S1.to_string()); print(S2); print(S3); print(S4)
