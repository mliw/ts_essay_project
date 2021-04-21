import pandas as pd
import numpy as np
import statsmodels.api as sm


def iterate_get_features(X,Y): # We've already added constant to X
    maintain_features = ["cpi_index_x","const"]
    model = sm.OLS(Y,X).fit()
    p_values = model.pvalues
    qualified_list = list(p_values.index[p_values<=0.05])
    result_list = list(set(maintain_features) | set(qualified_list))
    if len(result_list)==len(p_values):
        return result_list
    else:
        return iterate_get_features(X.loc[:,result_list],Y)


# 1 Build model from 2004-01(24) to 2020-02(217) (Make Prediction for certain time index)
data = pd.read_stata('data/output/result_data.dta')
del(data["level_0"])
timevary_result_data = data.copy()
timevary_result_data["timevary_forecast"] = np.nan
maintain_list = ['Int_Rate', 'Treasury_1', 'Treasury_5','Treasury_10', 'CSI_300','cpi_index_y',
       'cpi_index_x', 'd_M2', 'd_M1', 'd_M0']
data = data.loc[:,maintain_list]
data = sm.add_constant(data)

result = []
for i in range(24,218):
    print(i)
    tem_data = data.iloc[(i-24):i,:]
    tem_data.dropna(axis=0,inplace=True)
    X = tem_data.loc[:,['const','Int_Rate', 'Treasury_1', 'Treasury_5', 'Treasury_10', 'CSI_300', 'cpi_index_x', 'd_M2', 'd_M1', 'd_M0']]
    Y = tem_data.loc[:,["cpi_index_y"]]
    best_features = iterate_get_features(X,Y)
    model = sm.OLS(Y,X.loc[:,best_features]).fit()
    prediction_data = pd.DataFrame(data.loc[i,best_features])
    print(model.summary())
    timevary_result_data.loc[i,'timevary_forecast']=np.array(model.predict(prediction_data.T))[0]
    result.append([best_features,i])


with open('data/output/timevary_result.pkl', 'wb') as handle:
    pickle.dump(result, handle, protocol=2)   
with open('data/output/timevary_result.pkl', 'rb') as handle:
    variable_name=pickle.load(handle)   
timevary_result_data.to_csv("data/output/timevary_result_data.csv")
timevary_result_data.to_stata("data/output/timevary_result_data.dta")
# with open('path/file_name.pickle', 'wb') as handle:
#     pickle.dump(variable_name, handle, protocol=2)
# with open('path/file_name.pickle', 'rb') as handle:
#     variable_name=pickle.load(handle)
    