import pandas as pd
import datetime
import numpy as np


# 1 Deal with CPI
cpi = pd.read_excel('data/original_data/CPI.xlsx')
cpi = cpi.loc[cpi.loc[:,"Datasign"]=="C",:]
cpi.columns=['Date', 'Datasign', 'CPI']
my_logi = np.logical_and(cpi["Date"]>="2002-01",cpi["Date"]<="2021-02")
cpi = cpi.loc[my_logi,]
cpi.index = cpi.Date
del(cpi["Date"])
del(cpi["Datasign"])
# Generate result_cpi
time_index = []
for year in range(2002,2022):
    for month in range(1,13):
        my_str = str(year)+"-"+str(month) if month>=10 else str(year)+"-0"+str(month)
        time_index.append(my_str)
result_cpi = pd.DataFrame([],index = time_index)
result_cpi = pd.concat((result_cpi,cpi),axis = 1)
result_cpi = result_cpi.loc[result_cpi.index<="2021-02",]
result_cpi.fillna(0,inplace=True)
result_cpi["CPI"] = result_cpi["CPI"]/100
result_cpi["ratio"] = 1+result_cpi["CPI"] 
result_cpi.iloc[0,1] = 1
result_cpi["cpi_index"] = np.cumprod(result_cpi["ratio"])
del(result_cpi["CPI"])
del(result_cpi["ratio"])
# result_cpi is the finished data


# 2 Deal with other
other = pd.read_excel('data/original_data/other.xlsx')
def trans_str(my_date):
    return my_date.strftime("%Y-%m")
other["str_date"] = other["Date"].apply(trans_str)
other.index = other.str_date
del(other["Date"])
del(other["str_date"])
result = pd.concat((result_cpi,other),axis = 1)
# We get result at this stage


# 3 Deal with currency
currency = pd.read_excel('data/original_data/currency.xlsx')
currency.index = currency["Staper"]
del(currency["Staper"])
currency = currency.loc[currency.index>="2002-01",:]
result = pd.concat((result,currency),axis = 1)


# 4 Output data
def trans_year(my_str):
    return int(my_str.split("-")[0])
def trans_month(my_str):
    return int(my_str.split("-")[1])
result["date"] = result.index
result["year"] = result["date"].apply(trans_year)
result["month"] = result["date"].apply(trans_month)
result.columns = ['cpi_index', 'Int_Rate', 'Treasury_1',
       'Treasury_5', 'Treasury_10',
       'CSI_300', 'M2', 'M1', 'M0', 'date', 'year', 'month']
result.to_stata("data/finished_data/combined.dta")

























