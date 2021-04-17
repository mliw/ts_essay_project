//0 Load data and generate features
clear
use data/combined.dta
drop date
gen date = ym(year,month)
format date %tm
tsset date
gen cpi_index_y = 1200*ln(F12.cpi_index/cpi_index)/12-1200*ln(cpi_index/L1.cpi_index)
gen cpi_index_x = 1200*ln(cpi_index/L1.cpi_index)
//cpi_index_y is stationary
dfuller cpi_index_y, drift lags(14) regress
//cpi_index_x is stationary
dfuller cpi_index_x, drift lags(11) regress
//Int_Rate is stationary
dfuller Int_Rate, drift lags(2) regress
//Treasury_1 is stationary
dfuller Treasury_1, drift lags(1) regress
//Treasury_5 is stationary
dfuller Treasury_5, drift lags(1) regress
//Treasury_10 is stationary
dfuller Treasury_10, drift lags(1) regress
//CSI_300 is stationary
dfuller CSI_300, drift lags(9) regress
//M2 is NOT stationary
dfuller M2, drift lags(12) regress
gen ln_M2 = ln(M2)
gen d_M2 = D.ln_M2
drop ln_M2
drop M2
//d_M2 is stationary
dfuller d_M2, drift lags(15) regress
//M1 is NOT stationary
gen ln_M1 = ln(M1)
gen d_M1 = D.ln_M1
drop ln_M1
drop M1
//d_M1 is stationary
dfuller d_M1, drift lags(15) regress
//M0 is NOT stationary
gen ln_M0 = ln(M0)
gen d_M0 = D.ln_M0
drop ln_M0
drop M0
//d_M0 is stationary
dfuller d_M0, drift lags(15) regress


//1 Generate Nans value for out-of-sample prediction
gen benchmark_forecast = .
foreach var in Int_Rate	Treasury_1	Treasury_5	Treasury_10	CSI_300	d_M2 d_M1 d_M0{ 
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
foreach var in Int_Rate	Treasury_1	Treasury_5	Treasury_10	CSI_300	d_M2 d_M1 d_M0{ 
forvalues p = `=tm(2004m1)'/`=tm(2021m1)' {
qui regress cpi_index_y cpi_index_x `var' if date<`p' & date>=`p'-24
predict yhat,xb
replace `var'_forecast=yhat if date==`p'
drop yhat
}
}


//4 Save Data
save data/1_Make_Forecast.dta, replace


//giacross cpi_index_y CSI_300 benchmark_forecast, window(30) alpha(0.05) nw(3)
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
、、giacross cpi_index_y Treasury_10_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
