//0 Load data and generate features
clear
use data/output/timevary_result_data.dta
drop date
gen date = ym(year,month)
format date %tm
tsset date

giacross cpi_index_y timevary_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)

