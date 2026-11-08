# -*- coding: utf-8 -*-
"""Employees (雇用者, excluding the self-employed and family workers) by industry, annual averages.

Source: Statistics Bureau of Japan, Labour Force Survey (basic tabulation), 2025 annual average results,
結果の概要 (gaiyou.pdf, published January 2026), table I-8 主な産業別就業者数・雇用者数の推移, rows うち雇用者,
in 10 000 persons, 2015-2025 (time-series-linked values).
Cross-checked: 2023-2025 values agree with JILPT 'Hayawakari: employees by industry' (23g0005, 24g0005, 25g0005).
Used only for a sensitivity analysis replacing employed persons by employees as the denominator.
"""
import pandas as pd
yrs=list(range(2015,2026))
E={  # 万人
 '建設業':       [410,403,408,411,410,404,396,396,399,394,400],
 '製造業':       [988,1000,1008,1017,1021,1009,1007,1006,1021,1010,999],
 '情報通信業':   [201,200,204,211,219,229,244,258,263,274,283],
 '運輸業郵便業': [323,327,329,331,337,337,339,337,334,330,330],
 '卸売小売業':   [966,977,990,996,989,988,996,973,970,980,969],
 '金融保険業':   [150,160,165,162,164,164,165,157,154,153,155],
 '宿泊飲食':     [325,334,338,361,365,340,319,330,349,360,371],
 '教育学習支援業':[278,283,289,297,310,315,321,323,318,324,330],
 '医療福祉':     [754,779,787,805,818,837,859,876,881,892,917],
}
d=pd.DataFrame(E); d.insert(0,'year',yrs)
d.to_csv('data/employees_by_industry.csv',index=False); print(d.to_string(index=False))
