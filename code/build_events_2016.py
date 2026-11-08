# -*- coding: utf-8 -*-
"""出来事別 支給決定件数 FY2016-2025（群別）。
FY2016-2019：旧認定基準（平成23年基発1226第1号）の表2-8。出典：平成29年度版（FY2016,2017）、令和元年度版（FY2018,2019）
  ※平成30年度版でFY2017の値を照合。いずれも表画像を目視確認、合計は公表値と一致。
FY2020-2025：rosai_mental_by_event.csv（新基準、パワハラは2020年6月、カスハラは2023年9月に新設）。
群の定義：
  ハラスメント = 旧：(ひどい)嫌がらせ・いじめ・暴行 + セクハラ ／ 新：パワハラ + 同僚等からのいじめ・暴行 + セクハラ + カスハラ
  仕事量の変化、労働時間（月80時間以上の時間外 + 2週間以上の連続勤務）、事故・災害・傷病（重度の病気やケガ + 悲惨な事故・災害）、特別な出来事、その他 = 合計 − 上記
"""
import pandas as pd, numpy as np
D='data/'; O='output/intermediate/'
old={ # approvals
 2016:dict(bully=74,sexual=29,workload=63,h80=39,cont=47,ill=42,disaster=53,special=67,total=498),
 2017:dict(bully=88,sexual=35,workload=64,h80=41,cont=48,ill=26,disaster=63,special=63,total=506),
 2018:dict(bully=69,sexual=33,workload=69,h80=45,cont=25,ill=36,disaster=56,special=55,total=465),
 2019:dict(bully=79,sexual=42,workload=68,h80=32,cont=42,ill=28,disaster=55,special=63,total=509)}
nat=pd.read_csv(D+'rosai_mental_national.csv').set_index('fy')
for y,v in old.items(): assert v['total']==nat.loc[y,'approvals'],y
ev=pd.read_csv(D+'rosai_mental_by_event.csv'); pv=ev.pivot(index='event',columns='fy',values='approvals')
rows={}
for y,v in old.items():
    rows[y]={'Total':v['total'],'Harassment':v['bully']+v['sexual'],'Power harassment by supervisors':np.nan,'Bullying or violence (co-workers)':v['bully'],'Sexual harassment':v['sexual'],'Customer harassment':np.nan,
             'Change in workload':v['workload'],'Working hours':v['h80']+v['cont'],'Accidents, disasters, injury':v['ill']+v['disaster'],'Special events':v['special']}
for y in range(2020,2026):
    g=lambda k: int(pv.loc[k,y])
    H=g('パワハラ（上司等）')+g('同僚等からのいじめ・暴行')+g('セクハラ')+g('カスハラ（2023.9新設）')
    rows[y]={'Total':g('合計'),'Harassment':H,'Power harassment by supervisors':g('パワハラ（上司等）'),'Bullying or violence (co-workers)':g('同僚等からのいじめ・暴行'),'Sexual harassment':g('セクハラ'),'Customer harassment':g('カスハラ（2023.9新設）') if y>=2023 else np.nan,
             'Change in workload':g('仕事内容・仕事量の大きな変化'),'Working hours':g('月80時間以上の時間外労働')+g('2週間以上の連続勤務'),'Accidents, disasters, injury':g('悲惨な事故・災害の体験')+g('重度の病気やケガ'),'Special events':g('特別な出来事（極度の負荷等）')}
T=pd.DataFrame(rows)
T.loc['Other']=T.loc['Total']-T.loc[['Harassment','Change in workload','Working hours','Accidents, disasters, injury','Special events']].sum()
T.to_csv(O+'t24_events_2016_2025.csv'); print(T)
# Japanese-labelled t17 for figure compatibility
J=T.rename(index={'Harassment':'ハラスメント計','Change in workload':'仕事量の変化','Working hours':'長時間労働・連続勤務','Accidents, disasters, injury':'事故・災害・傷病','Special events':'特別な出来事','Other':'その他','Total':'合計'})
J.to_csv(O+'t17_events_approvals.csv')
