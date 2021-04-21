//0 Load data and generate features
clear
use data/output/result_data.dta
drop date
gen date = ym(year,month)
format date %tm
tsset date

giacross cpi_index_y Int_Rate_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/Int_Rate_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y Treasury_1_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/Treasury_1_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y Treasury_5_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/Treasury_5_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y Treasury_10_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/Treasury_10_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y CSI_300_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/CSI_300_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y d_M2_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/d_M2_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y d_M1_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/d_M1_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y d_M0_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/d_M0_forecast.jpg",as(jpg) name("Graph") quality(100)


giacross cpi_index_y machinelearning_out_of_sample benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/machinelearning_out_of_sample.jpg",as(jpg) name("Graph") quality(100)


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
//giacross cpi_index_y Treasury_10_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
//giacross cpi_index_y benchmark_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)