"""
Created on Sat Feb  5 13:17:56 2022

@author: baik6
"""

import os
import pandas as pd
import numpy as np
os.chdir('C:/Users/baik6/Desktop')
os.chdir('C:/Users/sthoy/바탕 화면/690 Industry Practicum/VeraBradley')
# read files

#pd.set_option('display.max_columns', 10)
#pd.set_option('display.max_rows', 10)


############### get product qty: web ###############
# read file
web = pd.read_csv('Webtransactions_clean.csv')

# change type / extract columns
web['DIM_SKU_KEY'] = web['DIM_SKU_KEY'].astype('str')
tmp = web.loc[:, ['DIM_SKU_KEY', 'ORDER_DATE', 'SALE_QUANTITY', 'NET_SALE_AMOUNT', 'DISCOUNT_AMOUNT', 'RETAIL_PRICE_AT_TRANSACTION']]

# group by qty
web_qty = tmp.groupby(tmp['DIM_SKU_KEY']).sum()

# save as csv
web_qty.to_csv('web_qty.csv')


############### get product qty: store ###############
# read file
store = pd.read_csv('st_yen.csv')

# change type / extract columns / rename column
tmp = store.loc[:, ['DIM_SKU_KEY', 'SALE_QUANTITY', 'NET_SALE_AMOUNT', 'SALE_DISCOUNT_AMOUNT', 'RETAIL_PRICE_AT_TRANSACTION']]
tmp['DIM_SKU_KEY'] = tmp['DIM_SKU_KEY'].astype('str')
tmp = tmp.rename(columns = {'SALE_DISCOUNT_AMOUNT': 'DISCOUNT_AMOUNT'})

# group by qty
store_qty = tmp.groupby(tmp['DIM_SKU_KEY']).sum()

# save as csv
store_qty.to_csv('store_qty.csv')


############### add product qty: web+store ###############
# read above file 
web_qty = pd.read_csv('web_qty.csv')
store_qty = pd.read_csv('store_qty.csv')

# concatenate two file / sum up qty
total = pd.concat([web_qty, store_qty], ignore_index=True)
total['DIM_SKU_KEY'] = total['DIM_SKU_KEY'].astype('str')
total_qty = total.groupby(total['DIM_SKU_KEY']).sum()


############### append sku info ###############
# read file
sku = pd.read_csv('Skus_clean.csv')

# sku: extract column / type transformation
skutmp = sku.loc[:, ['DIM_SKU_KEY', 'SKU', 'STYLE_DESCRIPTION', 'RETAIL_PRICE_CURRENT', 'STANDARD_COST_CURRENT', 'MERCHANT_BUSINESS_CATEGORY', 'MERCHANT_DEPARTMENT', 'MERCHANT_CLASS', 'PLM_COLOR_FAMILY', 'MERCHANT_PILLAR_DESCRIPTION']]
skutmp['DIM_SKU_KEY'] = skutmp['DIM_SKU_KEY'].astype('str')

# merge (join)
total_sales = pd.merge(total_qty, skutmp, on = 'DIM_SKU_KEY')

# order by net sales
total_sales = total_sales.sort_values('NET_SALE_AMOUNT', ascending=False)

# save as csv
#total_sales.to_csv('total_sales.csv')

#os.chdir('C:/Users/sthoy/IndustryPracticum_VeraBradley')
#total_sales = pd.read_csv('total_sales_sku.csv')
#total_sales['DIM_SKU_KEY'] = total_sales['DIM_SKU_KEY'].astype('str')

############### filter: zero-sales ###############
# drop rows: zero-or-minus sales
zero_dollar = total_sales[total_sales['NET_SALE_AMOUNT']<=0].index
tmp = total_sales.drop(zero_dollar)

# drop rows: e-gift card
giftcard = tmp[tmp['STYLE_DESCRIPTION']=='e-gift card'].index
tmp2 = tmp.drop(giftcard)
total_sales = tmp2


############### 1 ############### MERCHANT_CLASS ###############
# group/order by merchantclass (net sales) <-- type: series
by_mclass = total_sales.groupby(total_sales['MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending=False)

# change series to dataframe / set index
mclass_ratio = by_mclass['NET_SALE_AMOUNT'].to_frame()
mclass = mclass_ratio.rename_axis('MERCHANT_CLASS').reset_index()

# merge insignificant MERCHANT_CLASS group into 'others'
for i in range(len(mclass)):
    if mclass['NET_SALE_AMOUNT'][i] < 5.023208e+07:
        mclass['MERCHANT_CLASS'][i] = 'others'

tmp = mclass.groupby(mclass['MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending=False)
mclass_summary = tmp.rename_axis('MERCHANT_CLASS').reset_index()

# set ratio, label, color
label = mclass_summary['MERCHANT_CLASS'].values.tolist()
ratio = mclass_summary['NET_SALE_AMOUNT'].values.tolist()
color = ['#FDF5F7','#DB456C', '#E16585', '#E67E99', '#EB99AE', '#EEA8BA', '#F2BCCA', '#F5CBD6', '#F8DCE3','#FCEEF2']

# plot
import matplotlib.pyplot as plt
plt.pie(ratio, labels=label, startangle=2, colors=color, autopct='%.1f%%')
plt.title('Top 10 Sales Categories')
plt.legend(loc = (1, 0.5))
plt.show()

############### 2 ############### SOLID VS PATTERN by CATEGOREIS ###############
total_sales = pd.read_csv('total_sales_sku.csv')
total_sales['DIM_SKU_KEY'] = total_sales['DIM_SKU_KEY'].astype('str')

# create 'PATTERN' column: if pattern, 1 / solid, 0
total_sales['PATTERN'] = np.nan

for i in range(len(total_sales)):
    if total_sales['PLM_COLOR_FAMILY'][i]=='solid':
        total_sales['PATTERN'][i] = 0
    else:
        total_sales['PATTERN'][i] = 1

# get ratio of pattern by categories
total_sales['PATTERN_AMT'] = total_sales['NET_SALE_AMOUNT']*total_sales['PATTERN']
total_sales['PATTERN_QTY'] = total_sales['SALE_QUANTITY']*total_sales['PATTERN']

# average pattern ratio (total)
ttl_pt_amt = total_sales['PATTERN_AMT'].sum()
ttl_tt_amt = total_sales['NET_SALE_AMOUNT'].sum()
ttl_ptr_amt = ttl_pt_amt / ttl_tt_amt
print("Average Pattern Ratio (sales):", ttl_ptr_amt)

ttl_pt_qty = total_sales['PATTERN_QTY'].sum()
ttl_tt_qty = total_sales['SALE_QUANTITY'].sum()
ttl_ptr_qty = ttl_pt_qty / ttl_tt_qty
print("Average Pattern Ratio (qty):", ttl_ptr_qty)


# average pattern ratio (by categories)
tmp = total_sales.groupby(total_sales['MERCHANT_CLASS']).sum().sort_values('NET_SALE_AMOUNT', ascending=False)
tmp2 = tmp[['NET_SALE_AMOUNT', 'PATTERN_AMT', 'SALE_QUANTITY', 'PATTERN_QTY']] #.to_frame()
tmp3 = tmp2.rename_axis('MERCHANT_CLASS').reset_index()
tmp3['PATTERN_RATIO(AMT)'] = tmp3['PATTERN_AMT']/tmp3['NET_SALE_AMOUNT']
tmp3['PATTERN_RATIO(QTY)'] = tmp3['PATTERN_QTY']/tmp3['SALE_QUANTITY']
pattern = tmp3[['MERCHANT_CLASS','PATTERN_RATIO(AMT)','PATTERN_RATIO(QTY)']]
top10 = pattern.head(9)

bar_category = top10['MERCHANT_CLASS']
bar_value = top10['PATTERN_RATIO(AMT)']

color =['#EB99AE', '#EB99AE', '#EB99AE', '#DB456C', '#EB99AE', '#DB456C', '#DB456C', '#DB456C', '#EB99AE']
plt.barh(bar_category, bar_value, color = color)
plt.title('Pattern Ratio of Top 10 Item ($ Sales)')
plt.axvline(x=ttl_ptr_amt, linewidth=1, color='#DB456C')
plt.show()


############### 3 ############### SOLID VS PATTERN by YEARS ###############
############### get product qty: web ###############
# read file

os.chdir('C:/Users/sthoy/IndustryPracticum_VeraBradley')
web = pd.read_csv('Webtransactions_clean.csv')

# change type / extract columns
web['DIM_SKU_KEY'] = web['DIM_SKU_KEY'].astype('str')
tmp = web.loc[:, ['DIM_SKU_KEY', 'ORDER_DATE', 'SALE_QUANTITY', 'NET_SALE_AMOUNT', 'DISCOUNT_AMOUNT', 'RETAIL_PRICE_AT_TRANSACTION']]

# group by qty
web_qty = tmp.groupby(tmp['DIM_SKU_KEY']).sum()

# save as csv
web_qty.to_csv('web_qty.csv')


############### get product qty: store ###############
# read file
store = pd.read_csv('st_yen.csv')

# change type / extract columns / rename column
tmp = store.loc[:, ['DIM_SKU_KEY', 'SALE_QUANTITY', 'NET_SALE_AMOUNT', 'SALE_DISCOUNT_AMOUNT', 'RETAIL_PRICE_AT_TRANSACTION']]
tmp['DIM_SKU_KEY'] = tmp['DIM_SKU_KEY'].astype('str')
tmp = tmp.rename(columns = {'SALE_DISCOUNT_AMOUNT': 'DISCOUNT_AMOUNT'})

# group by qty
store_qty = tmp.groupby(tmp['DIM_SKU_KEY']).sum()

# save as csv
store_qty.to_csv('store_qty.csv')


############### add product qty: web+store ###############
# read above file 
web_qty = pd.read_csv('web_qty.csv')
store_qty = pd.read_csv('store_qty.csv')

# concatenate two file / sum up qty
total = pd.concat([web_qty, store_qty], ignore_index=True)
total['DIM_SKU_KEY'] = total['DIM_SKU_KEY'].astype('str')
total_qty = total.groupby(total['DIM_SKU_KEY']).sum()





### in specific merchan_class
### is there any more specific categories
### that shows spike in sales?