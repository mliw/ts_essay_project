**** JORDA_ROMER.DO

***  Valerie A. Ramey "Macroeconomic Shocks and Their Propagation" Handbook of Macroeconomics

*** Jorda method using Romer-Romer monetary shock - Figure 2B, part of Table 2 
***
*** Requires:
***     Monetarydat.xlsx

***************************************************************************************************


drop _all
clear all

set matsize 800
set mem 400m

capture log close
log using jorda_romer_results.log, replace

/*******************************************************************************
** RAW DATA IMPORTATION AND DATA SETUP

** SEE README SHEET OF EXCEL FILE FOR VARIABLE DEFINTIIONS
*******************************************************************************/

import Monetarydat_montly.dta

gen mdate = m(1959m1) + _n -1  //_n denotes current observation in stata

tsset mdate, m

drop if mdate<m(1969m3) //start in 1969 month 3

gen rrshockorig = D.cumrrshockorig

replace lip = 100*lip   
replace lcpi = 100*lcpi
replace lpcom = 100*lpcom

gen t = _n

/*******************************************************************************
**  SET UP FOR LATER IRF PLOTTING
*******************************************************************************/
foreach var in ffr lip lcpi unemp  { 
  quietly gen b`var' = .
  quietly gen up90b`var' = .
  quietly gen lo90b`var' = . 
} 

/*******************************************************************************
***  SET PARAMETERS THAT GOVERN SPECIFICATION
*******************************************************************************/

//Use updated RR shock: rrshock (available 1969-2007)

*******************************************************************************;

* ESTIMATE USING JORDA PROCEDURE AND GRAPH THE IRFS;

******************************************************************************;

gen h = t - 1  /* h is the horizon for the irfs */


forvalues i = 0/48 {

   foreach var in ffr lip lcpi unemp  {

      newey F`i'.`var' L(0/2).rrshock  L(0/2).lip L(0/2).unemp L(0/2).lcpi L(0/2).lpcom L(1/2).ffr , lag(`=`i' + 1')
	 
	  gen b`var'h`i' = _b[rrshock]
  
      gen se`var'h`i' = _se[rrshock]
  
	  quietly replace b`var' = b`var'h`i' if h==`i'
      quietly replace up90b`var' = b`var'h`i' + 1.68*se`var'h`i' if h==`i'
	  quietly replace lo90b`var' = b`var'h`i' - 1.68*se`var'h`i' if h==`i'

  }
}

*******************************************************************************;
**** Commment these commands out when q = 1;
replace blip = 0 if h==0
replace blcpi = 0 if h==0
replace bunemp = 0 if h==0

*******************************************************************************;

foreach var in ffr lip lcpi unemp  { 

tw (rarea up90b`var' lo90b`var' h, bcolor(gs14) clw(medthin medthin)) ///
  (scatter b`var' h, c(l) clp(l) ms(i) clc(black) mc(black) clw(medthick))if h<=48, saving(varromer_`var'.gph,replace)
}

graph combine varromer_ffr.gph varromer_lip.gph varromer_unemp.gph varromer_lcpi.gph 


outsheet h bffr lo90bffr up90bffr blip lo90blip up90blip bunemp lo90bunemp up90bunemp ///
 blcpi lo90blcpi up90blcpi using junk.csv if h<=48, replace comma 
 
/* Note that I copied this .csv file and pasted it into
  Monetary_irfs.xlsx to create nicer looking graphs in Stata.  In some cases,
  I normalized responses.*/

}

capture log close;
