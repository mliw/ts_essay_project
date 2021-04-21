import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import hyperopt
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
import pickle
N_FOLDS = 5


# Return mean-squared errors
def produce_holdout(model,total_data_cache):    
    train_x = total_data_cache[0].copy()
    train_y = total_data_cache[1].copy()
    train_x = pd.DataFrame(train_x)
    train_y = pd.DataFrame(train_y)
    kf = KFold(N_FOLDS, shuffle=True, random_state=42)
    kf.get_n_splits(train_x,train_y)   
    result = []
    for train_index, test_index in kf.split(train_x, train_y):
        tem_train_x, tem_train_y = train_x.iloc[train_index,:], train_y.iloc[train_index,:]
        tem_test_x, tem_test_y = train_x.iloc[test_index,:], train_y.iloc[test_index,:] 
        tem_train_y = tem_train_y.values.reshape(-1)           
        model.fit(tem_train_x,tem_train_y)
        prediction = model.predict(tem_test_x)
        result.append(np.sqrt(mean_squared_error(tem_test_y,prediction)))
    return result


# Return the mean of mean-squared errors
def nm_penalty(model,total_data_cache):
    train_x = total_data_cache[0].copy()
    train_y = total_data_cache[1].copy()
    train_x = pd.DataFrame(train_x)
    train_y = pd.DataFrame(train_y)  
    holdout = produce_holdout(model,total_data_cache)
    result = np.mean(holdout)+np.std(holdout)
    return result


# Objective function for tunning parameters
def objective(param):
    tuning_pipeline = XGBRegressor(**param)
    loss = nm_penalty(tuning_pipeline,[tunning_train_x,train_y])
    return loss  


# Extract best parameter
def change_best_XGBRegressor(best_p):
    best = best_p.copy()
    best["max_depth"]+=1    
    best["n_estimators"]+=1  
    best["n_jobs"]=2
    best["random_state"]=1
    best["objective"]="reg:squarederror"
    return best


# Parameter Space
XGBRegressor_dic = {
    'reg_alpha': hyperopt.hp.uniform('reg_alpha',0,2),
    'reg_lambda': hyperopt.hp.uniform('reg_lambda',0,2),
    'n_jobs': hyperopt.hp.choice('n_jobs',[2]),
    'objective': hyperopt.hp.choice('objective',["reg:squarederror"]),
    'random_state': hyperopt.hp.choice('random_state',[1]),
    'max_depth': hyperopt.hp.randint('max_depth',11)+1, 
    'n_estimators': hyperopt.hp.randint('n_estimators',25)+1,    
}


# 1 Build model from 2004-01(24) to 2020-02(217) (Make Prediction for certain time index)
data = pd.read_stata('data/1_Make_Forecast.dta')
result_data = data.copy()
date_index = data["index"]
maintain_list = ['Int_Rate', 'Treasury_1', 'Treasury_5','Treasury_10', 'CSI_300','cpi_index_y',
       'cpi_index_x', 'd_M2', 'd_M1', 'd_M0']
data = data.loc[:,maintain_list]
result_data["machinelearning_out_of_sample"] = np.nan
# 1_1 Train on a batch
# Record feature_combined(The relative importance of different features)
# Record i(the timeindex for forecast)
result = []
for i in range(24,218):
    print(i)
    tem_data = data.iloc[(i-24):i,:]
    tem_data.dropna(axis=0,inplace=True)
    initial_xgb = XGBRegressor(random_state=1,objective="reg:squarederror",n_jobs=2)
    X = tem_data.loc[:,['Int_Rate', 'Treasury_1', 'Treasury_5', 'Treasury_10', 'CSI_300', 'cpi_index_x', 'd_M2', 'd_M1', 'd_M0']]
    Y = tem_data.loc[:,["cpi_index_y"]]
    initial_xgb.fit(X,Y)
    feature_importance = initial_xgb.feature_importances_
    features = X.columns
    feature_combined = pd.DataFrame([features,feature_importance]).T
    feature_combined.columns = ["feature","score"]
    feature_combined = feature_combined.iloc[np.argsort(feature_importance)[::-1],:]
    sorted_features = np.array(feature_combined["feature"])
    best_record_i = []
    for num_feature in range(1,feature_combined.shape[0]+1):      
        test_features = sorted_features[:num_feature]          
        # Tunning model_para
        tunning_train_x = X.loc[:,test_features] 
        train_y = Y 
        trials = hyperopt.Trials()
        best = hyperopt.fmin(objective,
        space=XGBRegressor_dic,
        algo=hyperopt.tpe.suggest,
        max_evals=70,
        rstate = np.random.RandomState(12),
        trials=trials)  
        best_param = change_best_XGBRegressor(best)
        best_model = XGBRegressor(**best_param)
        best_score = nm_penalty(best_model,[tunning_train_x,train_y])
        best_record_i.append([test_features,best_param,best_score])
    best_model_combined = sorted(best_record_i, key=lambda x:  x[-1], reverse=False)[0]
    best_model_combined.append(feature_combined)
    best_model_combined.append(i)
    forecast_model = XGBRegressor(**best_model_combined[1])
    forecast_model.fit(X.loc[:,best_model_combined[0]],Y)
    prediction_data = pd.DataFrame(data.loc[i,best_model_combined[0]])
    result_data.loc[i,'machinelearning_out_of_sample']=forecast_model.predict(prediction_data.T)[0]
    result.append(best_model_combined)
    
with open('data/output/machine_learning_result.pkl', 'wb') as handle:
    pickle.dump(result, handle, protocol=2)   
with open('data/output/machine_learning_result.pkl', 'rb') as handle:
    variable_name=pickle.load(handle)   
result_data.to_csv("data/output/result_data.csv")
result_data.to_stata("data/output/result_data.dta")
# with open('path/file_name.pickle', 'wb') as handle:
#     pickle.dump(variable_name, handle, protocol=2)
# with open('path/file_name.pickle', 'rb') as handle:
#     variable_name=pickle.load(handle)
    