# -*- coding: utf-8 -*-
"""追加転記 FY2016-2020：精神障害の業種別請求（FY2016-17）、脳・心臓疾患の業種別請求・支給決定（FY2016-20）
出典（いずれも厚生労働省「過労死等の労災補償状況」表1-2・表2-2、各報告は前年度と当年度の2列を掲載）
  平成29年度版 https://www.mhlw.go.jp/content/12602000/000333800.pdf  → FY2016, FY2017
  平成30年度版 https://www.mhlw.go.jp/content/11601000/000577651.pdf  → FY2017（照合）, FY2018
  令和2年度版 別添資料1 https://www.mhlw.go.jp/content/11402000/000796021.pdf（Internet Archive 2021-06-26） → FY2019, FY2020
全て表画像を目視で確認し、業種合計が全国合計と一致することをassertで検証。
"""
import pandas as pd
D='data/'
ind=['農林漁鉱','製造業','建設業','運輸業郵便業','卸売小売業','金融保険業','教育学習支援業','医療福祉','情報通信業','宿泊飲食','その他(サービス業含む)','合計']
mental_claims={2016:[11,279,108,173,220,55,42,302,82,81,233,1586],
               2017:[10,308,114,161,232,63,51,313,111,74,295,1732]}
cvd={2016:{'claims':[12,101,98,212,106,7,12,47,22,50,158,825],'approvals':[5,41,18,97,29,1,3,10,9,20,27,260]},
     2017:{'claims':[5,110,112,188,115,10,15,43,26,61,155,840],'approvals':[3,24,17,99,35,0,3,2,6,28,36,253]},
     2018:{'claims':[12,105,99,197,111,9,20,62,24,76,162,877],'approvals':[4,28,14,94,24,1,2,6,4,32,29,238]},
     2019:{'claims':[20,99,130,197,150,9,14,55,21,63,178,936],'approvals':[6,22,17,68,32,1,2,5,5,21,37,216]},
     2020:{'claims':[11,92,108,158,111,13,13,67,23,31,157,784],'approvals':[5,17,27,58,38,0,2,8,2,15,22,194]}}
df=pd.read_csv(D+'rosai_mental_by_industry.csv')
for y,v in mental_claims.items():
    assert sum(v[:-1])==v[-1],(y,'mental')
    for i,n in zip(ind,v): df.loc[(df.fy==y)&(df.industry==i),'claims']=n
df.to_csv(D+'rosai_mental_by_industry.csv',index=False)
# national claims check
nat=pd.read_csv(D+'rosai_mental_national.csv').set_index('fy')
for y,v in mental_claims.items(): assert nat.loc[y,'claims']==v[-1],(y,nat.loc[y,'claims'])
c=pd.read_csv(D+'rosai_cvd_by_industry.csv'); c=c[~c.fy.isin(cvd.keys())]
rows=[]
for y,d in cvd.items():
    for k in ['claims','approvals']: assert sum(d[k][:-1])==d[k][-1],(y,k)
    for j,i in enumerate(ind): rows.append({'fy':y,'industry':i,'cvd_claims':d['claims'][j],'cvd_approvals':d['approvals'][j]})
c=pd.concat([pd.DataFrame(rows),c]).sort_values(['fy']).reset_index(drop=True)
c.to_csv(D+'rosai_cvd_by_industry.csv',index=False)
print(c.groupby('fy').size(), c[c.industry=='合計'])
