import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt


# 1 Draw heatma
maintain_list = ['Int_Rate', 'Treasury_1', 'Treasury_5','Treasury_10', 'CSI_300',
       'cpi_index_x', 'd_M2', 'd_M1', 'd_M0']
with open('data/output/machine_learning_result.pkl', 'rb') as handle:
    variable_name=pickle.load(handle) 
pic_data = pd.DataFrame(np.zeros((len(variable_name),len(maintain_list))),columns=maintain_list)

for i in range(len(variable_name)):
    tem = list(variable_name[i][0].copy())
    pic_data.loc[i,tem]=1
    
heat_plot=sns.heatmap(data=pic_data.T,cmap="YlGnBu",xticklabels=False,cbar=False)
plt.savefig("pics/machinelearning_heat_plot.png",dpi=400,bbox_inches='tight')
plt.close()


# 2 Draw feature importance
pic_data = pd.DataFrame(np.zeros((len(variable_name),len(maintain_list))),columns=maintain_list)
rank_names = pic_data.columns 

for i in range(len(variable_name)):   
    tem = variable_name[i][3]
    tem.index = tem["feature"]
    pic_data.loc[i,:] = tem.loc[rank_names,"score"]
dti = pd.date_range("2004-01-01", periods=194, freq='M')
pic_data.index = dti
line_plot = sns.lineplot(data=pic_data.iloc[:,:6])
plt.savefig("pics/machinelearning_featureimportance.png",dpi=400,bbox_inches='tight')
plt.close()

 