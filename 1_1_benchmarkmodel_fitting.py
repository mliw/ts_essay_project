import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

# 1 Build model from 2004-01(24) to 2020-02(217) (Make Prediction for certain time index)
data = pd.read_stata('data/output/result_data.dta')
del(data["level_0"])
timevary_result_data = data.copy()
timevary_result_data["timevary_forecast"] = np.nan
maintain_list = ['cpi_index_y','cpi_index_x']
data = data.loc[:,maintain_list]
data = sm.add_constant(data)

result = []
for i in range(24,218):
    print(i)
    tem_data = data.iloc[(i-24):i,:]
    tem_data.dropna(axis=0,inplace=True)
    X = tem_data.loc[:,['const','cpi_index_x']]
    Y = tem_data.loc[:,["cpi_index_y"]]
    model = sm.OLS(Y,X).fit()
    result.append([i,model.rsquared])

dti = pd.date_range("2004-01-01", periods=194, freq='M')
result = pd.DataFrame(result,columns=["index","R-squared"])
result["time_index"] = dti
sns.set()
line_plot=sns.lineplot(data=result,x="time_index",y="R-squared")
plt.savefig("pics/benchmark_model_R_squared.png",dpi=400)
