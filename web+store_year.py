# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import numpy as np
os.chdir('C:/Users/baik6/Downloads')
total = pd.read_csv('web+store_year.csv')

# type transformation
total['DIM_SKU_KEY'] = total['DIM_SKU_KEY'].astype('str')
total['ORDER_DATE'] = total['ORDER_DATE'].astype('datetime64[ns]')
total['YEAR'] = total['ORDER_DATE'].dt.year

# group by: year, sku
tmp = total.groupby(['YEAR', 'DIM_SKU_KEY']).sum()
tmp2 = tmp.reset_index()

# append sku
skutmp = pd.read_csv('Skus_clean.csv')
skutmp['DIM_SKU_KEY'] = skutmp['DIM_SKU_KEY'].astype('str')
skutmp = skutmp.loc[:, ['DIM_SKU_KEY', 'STYLE_DESCRIPTION','RETAIL_PRICE_CURRENT', 'STANDARD_COST_CURRENT', 'MERCHANT_BUSINESS_CATEGORY', 'MERCHANT_DEPARTMENT','MERCHANT_CLASS','PLM_COLOR_FAMILY']]

skutmp['PATTERN'] = np.nan

for i in range(len(skutmp)):

    if skutmp['PLM_COLOR_FAMILY'][i] == 'solid':
        skutmp['PATTERN'][i] = 0

    else:
        skutmp['PATTERN'][i] = 1
 

year_sku = pd.merge(tmp2, skutmp, on = 'DIM_SKU_KEY')

# drop: zero sales, e-gift card
zero_dollar = year_sku[year_sku['NET_SALE_AMOUNT'] <= 0].index
giftcard = year_sku[year_sku['STYLE_DESCRIPTION']=='e-gift card'].index

tmp3 = year_sku.drop(zero_dollar)
tmp4 = tmp3.drop(giftcard)


tmp4['PATTERN_AMT'] = tmp4['NET_SALE_AMOUNT']*tmp4['PATTERN']
tmp4['PATTERN_QTY'] = tmp4['SALE_QUANTITY']*tmp4['PATTERN']

year_2018 = tmp4[tmp4['YEAR'] == 2018].groupby(['YEAR','MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending = False)
#year_2018['PATTERN_RATIO(AMT)'] = year_2018['PATTERN_AMT']/year_2018['NET_SALE_AMOUNT']
#year_2018['PATTERN_RATIO(QTY)'] = year_2018['PATTERN_QTY']/year_2018['SALE_QUANTITY']
y2018 = year_2018.rename_axis(['YEAR','MERCHANT_CLASS']).reset_index()

year_2019 = tmp4[tmp4['YEAR'] == 2019].groupby(['YEAR','MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending = False)
#year_2019['PATTERN_RATIO(AMT)'] = year_2019['PATTERN_AMT']/year_2019['NET_SALE_AMOUNT']
#year_2019['PATTERN_RATIO(QTY)'] = year_2019['PATTERN_QTY']/year_2019['SALE_QUANTITY']
y2019 = year_2019.rename_axis(['YEAR','MERCHANT_CLASS']).reset_index()

year_2020 = tmp4[tmp4['YEAR'] == 2020].groupby(['YEAR','MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending = False)
#year_2020['PATTERN_RATIO(AMT)'] = year_2020['PATTERN_AMT']/year_2020['NET_SALE_AMOUNT']
#year_2020['PATTERN_RATIO(QTY)'] = year_2020['PATTERN_QTY']/year_2020['SALE_QUANTITY']
y2020 = year_2020.rename_axis(['YEAR','MERCHANT_CLASS']).reset_index()

year_2021 = tmp4[tmp4['YEAR'] == 2021].groupby(['YEAR','MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending = False)
#year_2021['PATTERN_RATIO(AMT)'] = year_2021['PATTERN_AMT']/year_2021['NET_SALE_AMOUNT']
#year_2021['PATTERN_RATIO(QTY)'] = year_2021['PATTERN_QTY']/year_2021['SALE_QUANTITY']
y2021 = year_2021.rename_axis(['YEAR','MERCHANT_CLASS']).reset_index()

y2018 = pd.read_csv('2018.csv')
y2019 = pd.read_csv('2019.csv')
y2020 = pd.read_csv('2020.csv')
y2021 = pd.read_csv('2021.csv')

for i in range(len(y2018)):

    if y2018['NET_SALE_AMOUNT'][i] < 14674205.47:
        y2018['MERCHANT_CLASS'][i] = 'others'


for i in range(len(y2019)):

    if y2019['NET_SALE_AMOUNT'][i] < 1.591705e+07:
        y2019['MERCHANT_CLASS'][i] = 'others'

for i in range(len(y2020)):

    if y2020['NET_SALE_AMOUNT'][i] < 1.142236e+07:
        y2020['MERCHANT_CLASS'][i] = 'others'

for i in range(len(y2021)):

    if y2021['NET_SALE_AMOUNT'][i] < 14220384.05:
        y2021['MERCHANT_CLASS'][i] = 'others'
        
tmp2018 = y2018.groupby(y2018['MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending=False)
summary2018 = tmp2018.rename_axis('MERCHANT_CLASS').reset_index()
summary2018['PATTERN_RATIO(AMT)'] = summary2018['PATTERN_AMT']/summary2018['NET_SALE_AMOUNT']
summary2018['PATTERN_RATIO(QTY)'] = summary2018['PATTERN_QTY']/summary2018['SALE_QUANTITY']
summary18 = summary2018[['YEAR','MERCHANT_CLASS','PATTERN_RATIO(AMT)']]
summary18['YEAR'] = 2018

tmp2019 = y2019.groupby(y2018['MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending=False)
summary2019 = tmp2019.rename_axis('MERCHANT_CLASS').reset_index()
summary2019['PATTERN_RATIO(AMT)'] = summary2019['PATTERN_AMT']/summary2019['NET_SALE_AMOUNT']
summary2019['PATTERN_RATIO(QTY)'] = summary2019['PATTERN_QTY']/summary2019['SALE_QUANTITY']
summary19 = summary2019[['YEAR','MERCHANT_CLASS','PATTERN_RATIO(AMT)']]
summary19['YEAR'] = 2019

tmp2020 = y2020.groupby(y2018['MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending=False)
summary2020 = tmp2020.rename_axis('MERCHANT_CLASS').reset_index()
summary2020['PATTERN_RATIO(AMT)'] = summary2020['PATTERN_AMT']/summary2020['NET_SALE_AMOUNT']
summary2020['PATTERN_RATIO(QTY)'] = summary2020['PATTERN_QTY']/summary2020['SALE_QUANTITY']
summary20 = summary2020[['YEAR','MERCHANT_CLASS','PATTERN_RATIO(AMT)']]
summary20['YEAR'] = 2020

tmp2021 = y2021.groupby(y2018['MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending=False)
summary2021 = tmp2021.rename_axis('MERCHANT_CLASS').reset_index()
summary2021['PATTERN_RATIO(AMT)'] = summary2021['PATTERN_AMT']/summary2021['NET_SALE_AMOUNT']
summary2021['PATTERN_RATIO(QTY)'] = summary2021['PATTERN_QTY']/summary2021['SALE_QUANTITY']
summary21 = summary2021[['YEAR','MERCHANT_CLASS','PATTERN_RATIO(AMT)']]
summary21['YEAR'] = 2021

summary_ttl = pd.concat([summary18, summary19, summary20, summary21], ignore_index=True)

crsbdy = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'crossbodies']
trvbag = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'travel bags']
bacpak = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'backpacks']
totes = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'totes']
textil = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'textiles']
cosmet = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'cosmetics']
keychn = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'ids/keychains']
trvacc = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'travel/packing accessories']
others = summary_ttl.loc[summary_ttl['MERCHANT_CLASS']== 'others']
years = summary_ttl['YEAR'].unique()

import matplotlib.pyplot as plt

crsbdy = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "crossbodies"].iloc[:,2]
trvbag = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "travel bags"].iloc[:,2]
bacpak = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "backpacks"].iloc[:,2]
totes = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "totes"].iloc[:,2]
textil = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "textiles"].iloc[:,2]
cosmet = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "cosmetics"].iloc[:,2]
keychn = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "ids/keychains"].iloc[:,2]
trvacc = summary_ttl[summary_ttl['MERCHANT_CLASS'] == "travel/packing accessories"].iloc[:,2]

fig = plt.figure(figsize=(8,8))
fig.set_facecolor('white')
ax = fig.add_subplot()

ax.plot(years, crsbdy, marker='o', label='crossbodies')
ax.plot(years, trvbag, marker='o', label='travel bags') 
ax.plot(years, bacpak, marker='o', label='backpacks') 
ax.plot(years, totes, marker='o', label='totes') 
ax.plot(years, textil, marker='o', label='textiles') 
ax.plot(years, cosmet, marker='o', label='cosmetics') 
ax.plot(years, keychn, marker='o', label='ids/keychains') 
ax.plot(years, trvacc, marker='o', label='travel/packing accessories') 
ax.plot(years, avg, marker='o', label='average')

plt.legend()

avg = []
avg.append(summary2018['PATTERN_AMT'].sum()/summary2018['NET_SALE_AMOUNT'].sum())
avg.append(summary2019['PATTERN_AMT'].sum()/summary2019['NET_SALE_AMOUNT'].sum())
avg.append(summary2020['PATTERN_AMT'].sum()/summary2020['NET_SALE_AMOUNT'].sum())
avg.append(summary2021['PATTERN_AMT'].sum()/summary2021['NET_SALE_AMOUNT'].sum())

