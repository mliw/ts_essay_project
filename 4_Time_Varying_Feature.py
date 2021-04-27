import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt


maintain_list = ['Int_Rate', 'Treasury_1', 'Treasury_5','Treasury_10', 'CSI_300',
       'cpi_index_x', 'd_M2', 'd_M1', 'd_M0']
with open('data/output/timevary_result.pkl', 'rb') as handle:
    variable_name=pickle.load(handle) 
pic_data = pd.DataFrame(np.zeros((len(variable_name),len(maintain_list))),columns=maintain_list)

for i in range(len(variable_name)):
    tem = variable_name[i][0].copy()
    tem.remove('const')
    pic_data.loc[i,tem]=1
    
heat_plot=sns.heatmap(data=pic_data.T,cmap="YlGnBu",xticklabels=False,cbar=False)
plt.savefig("pics/timevary_heat_plot.png",dpi=400,bbox_inches='tight')
plt.close()

pic_data = pd.DataFrame(np.zeros((len(variable_name),len(maintain_list))),columns=maintain_list)
pic_data["cpi_index_x"] = 1    
heat_plot=sns.heatmap(data=pic_data.T,cmap="YlGnBu",xticklabels=False,cbar=False)
plt.savefig("pics/benchmark_heat_plot.png",dpi=400,bbox_inches='tight')
plt.close()
