import pandas as pd
import numpy as np


# 1 check model from 2004-01(24) to 2020-02(217) (Make Prediction for certain time index)
data = pd.read_stata('data/output/timevary_result_data.dta')
del(data["level_0"])
data = data.iloc[24:218,:]

# 1_1 generate check list and abs_err
check_list = ['benchmark_forecast','Int_Rate_forecast', 'Treasury_1_forecast', 'Treasury_5_forecast',
       'Treasury_10_forecast', 'CSI_300_forecast', 'd_M2_forecast','d_M1_forecast', 'd_M0_forecast', 'machinelearning_out_of_sample',
       'timevary_forecast']
def gen_abs_err(data,check_name):
    abs_err = np.abs(data[check_name]-data["cpi_index_y"])
    data[check_name+"_abs_err"]=abs_err
for items in check_list:
    gen_abs_err(data,items)

# 1_2 generate time-reversal point
compare_list = ['Int_Rate_forecast_abs_err', 'Treasury_1_forecast_abs_err',
       'Treasury_5_forecast_abs_err', 'Treasury_10_forecast_abs_err',
       'CSI_300_forecast_abs_err', 'd_M2_forecast_abs_err',
       'd_M1_forecast_abs_err', 'd_M0_forecast_abs_err',
       'machinelearning_out_of_sample_abs_err', 'timevary_forecast_abs_err']    
def gen_LM2(data,compare_name):
    err_difference = data[compare_name]-data['benchmark_forecast_abs_err']
    P = len(err_difference)
    cumsum_err_difference = np.cumsum(err_difference)
    n_time = np.arange(P)+1
    mean_err_difference = np.mean(err_difference)
    latter_part = np.abs(cumsum_err_difference-mean_err_difference*n_time)
    break_point = np.argmax(np.array(latter_part))
    path_left = np.mean(err_difference[:break_point])
    path_right = np.mean(err_difference[break_point:])
    date_list = np.array(data["index"])
    situation = "worse after break point" if path_right>path_left else "better after break point"
    return [compare_name.replace("_abs_err",""),date_list[break_point],situation]

result = []
for compare_name in  compare_list:
    result.append(gen_LM2(data,compare_name))
result = pd.DataFrame(result,columns=["Model Type","Break Point","Performance"])
result.to_csv("data/output/onetime-reversal.csv")
    
    
