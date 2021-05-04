import pandas as pd
import numpy as np
from xlrd import open_workbook


# 1 Load the data we already have
data_1 = pd.read_stata("data/output/timevary_result_data.dta")
del(data_1["level_0"])

# 2 Load the data of ffr
workbook  = open_workbook('data/FEDFUNDS.xls')
sheet = workbook.sheet_by_index(0)
ffr = sheet.col_values(1)
ffr = np.array(ffr[1:])
dti = pd.date_range("1954-07-01", periods=len(ffr), freq='M')
ffr_frame = pd.DataFrame([dti,ffr]).T
data_1["ffr"] = np.array(ffr_frame.iloc[570:800,1]).astype(np.float32)

# 3 Save data
data_1.to_stata("data/output/ffr_timevary_result_data.dta")