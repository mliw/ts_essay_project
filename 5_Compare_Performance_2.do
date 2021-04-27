//0 Load data and generate features
clear
use data/output/timevary_result_data.dta
drop date
gen date = ym(year,month)
format date %tm
tsset date

giacross cpi_index_y timevary_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/timevary_forecast.jpg",as(jpg) name("Graph") quality(100)

giacross cpi_index_y timevary_forecast Treasury_10_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/timevary_forecast_treasury10.jpg",as(jpg) name("Graph") quality(100)

giacross cpi_index_y timevary_forecast benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/timevary_forecast.jpg",as(jpg) name("Graph") quality(100)

giacross cpi_index_y machinelearning_out_of_sample benchmark_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/machinelearning_out_of_sample.jpg",as(jpg) name("Graph") quality(100)

giacross cpi_index_y machinelearning_out_of_sample Treasury_10_forecast, window(30) alpha(0.05) nw(3)
graph export "pics/machinelearning_out_of_sample_treasury10.jpg",as(jpg) name("Graph") quality(100)

