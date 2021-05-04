//0 Load data and generate features
clear
use data/output/ffr_timevary_result_data.dta
drop date
gen date = ym(year,month)
format date %tm
tsset date

//1 Generate Nans value for out-of-sample prediction
quietly gen ffr_forecast = .

//2 Get out_of_sample_prediction based on other factors
forvalues p = `=tm(2004m1)'/`=tm(2021m1)' {
qui regress cpi_index_y cpi_index_x ffr if date<`p' & date>=`p'-24
predict yhat,xb
replace ffr_forecast=yhat if date==`p'
drop yhat
}

// ffr vs benchmark
giacross cpi_index_y ffr_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/ffr_benchmark.jpg",as(jpg) name("Graph") quality(100)

// ffr vs Int_Rate
giacross cpi_index_y ffr_forecast Int_Rate_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/ffr_Int_Rate.jpg",as(jpg) name("Graph") quality(100)
