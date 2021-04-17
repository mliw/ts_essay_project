//0 Load data and generate features
clear
use data/combined.dta
drop date
gen date = ym(year,month)
format date %tm
tsset date
gen cpi_index_y = 1200*ln(F12.cpi_index/cpi_index)/12-1200*ln(cpi_index/L1.cpi_index)
gen cpi_index_x = 1200*ln(cpi_index/L1.cpi_index)
//Both of them are stationary(dfuller test)
//qui dfuller cpi_index_y, drift lags(14) regress
//qui dfuller cpi_index_x, drift lags(11) regress


//1 Generate Nans value for out-of-sample prediction
gen benchmark_forecast = .
foreach var in Int_Rate	Treasury_1	Treasury_5	Treasury_10	CSI_300	M2	M1	M0{ 
  quietly gen `var'_forecast = .
} 


//2 Get out_of_sample_prediction for benchmark_forecast
forvalues p = `=tm(2004m1)'/`=tm(2021m1)' {
qui regress cpi_index_y L(0/0).cpi_index_x	if date<`p' & date>=`p'-24
predict yhat,xb
replace benchmark_forecast=yhat if date==`p'
drop yhat
}


//3 Get out_of_sample_prediction based on other factors
foreach var in Int_Rate	Treasury_1	Treasury_5	Treasury_10	CSI_300	M2	M1	M0{ 
forvalues p = `=tm(2004m1)'/`=tm(2021m1)' {
qui regress cpi_index_y cpi_index_x `var' if date<`p' & date>=`p'-24
predict yhat,xb
replace `var'_forecast=yhat if date==`p'
drop yhat
}
}


//4 Save Data
save data/1_Make_Forecast.dta, replace

 

//scalar best_lags = .
//scalar best_BIC = .
//forvalues i = 0/10 {
//	qui regress cpi_index_y L(0/`i').cpi_index_x if date<p & date>=p-24
//	qui estat ic
//	scalar model_BIC = r(S)[1,6]
//	di `i'
//	di model_BIC
//	if model_BIC<best_BIC {
//	scalar best_BIC = model_BIC
//	scalar best_lags = `i'
//	}
//	regress cpi_index_y L(0/1).cpi_index_x if date<p & date>=p-24
//}