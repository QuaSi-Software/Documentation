# Validation

In this section, the validation of single components of ReSiE is described. A validation of further detailed components and of whole energy systems will follow.

## Components
### Geothermal probe

The implementation of the model of the geothermal probes, as described in the corresponding chapter in "Technical description", has been validated against measurement data and the commercial, widely used software Energy Earth Designer (EED) that uses a similar approach with g-functions as the model in ReSiE does. 
As measurement data, the project "GEW" in Gelsenkirchen, Germany was used. The monitoring project is described in detail in the publication Bockelmann2021[^Bockelmann2021]. Here, a probe field with 36 probes is investigated, including regeneration of the geothermal probe field using a reverible heat pump. For the validation presented here, the input and output energy of the year 2014 into and out of the probe field were taken as inputs in EED and ReSiE, and the resulting average fluid temperature within the probe field was compared. Also, but not shown here, the model in ReSiE was adjusted to follow the average probe field temperature measured, and the resulting energy in- and output was compared to the measurement data. As this needed adaption of the simulation model that is now not included within ReSiE, this is not further described here.

[^Bockelmann2021]: Bockelmann, Franziska: IEA HPT Annex 52 - Long-term performance monitoring of GSHP systems for commercial, institutional and multi-family buildings: Case study report for GEW, Germany, 2021, Braunschweig.

The 36 probes of the irregular shaped probe field were approximated using a recangle shape with 3 x 12 probes with a distance of 9 m each. The g-function for this probe field was taken from the open source library by Spitler and Cook[^Spitler,Cook]. The thermal properies of the soil are known from a thermal response test at the site. 

[^Spitler,Cook]: J. D. Spitler, J. C. Cook, T. West, and X. Liu:  G-Function Library for Modeling Vertical Bore Ground Heat Exchanger. Geothermal Data Repository, 2021. doi: [https://doi.org/10.15121/1811518](https://doi.org/10.15121/1811518).

The results showed a high sensibility to the undisturbed ground temperature and also to the temperature spread that is assumed for the energy loding and unloading of the probe field, as this directly affects the velocity of the fliud in the pipes and therefore the energy flow into or out of the soil. In the case study investigated, the power of the regeneration was much higher than the power of heat extraction, and therefore the temeperature spread of loading had to be adjusted to meet the reality. This was also caused from the fact that the probe field is highly oversized for the energy demand. The maximal output and input power was set very high to not limit the external energy sink and source into and out of the probe field.

For a better overview, the daily averaged mean temperature within the probe field is compared betweeen ReSiE, EED and the measurement data in the following figure. The mean temperature difference (absolute, 1h time step, in the year 2014) between ReSiE and EED is 0.35 K (max. 7.3 K) and 0.55 K (max. 1.6 K) between ReSiE and the measurement data.

![Validation of probe model with measurement data and EED: Average fluid temperature daily](fig/240402_probe_compare_EED_Measurement_ReSiE_GEW2014_daily.svg)

Here, one week of the figure above is plotted with a higher temporal resolution of one hour:

![Validation of probe model with measurement data and EED: Average fluid temperature hourly](fig/240402_probe_compare_EED_Measurement_ReSiE_GEW2014_hourly.svg)


Also, a simulation performed with different time steps has been compared, from 15 minutes to 4 hours, showing only slight and expected differences in the average fluid temperature, caused by the different time resolution.

