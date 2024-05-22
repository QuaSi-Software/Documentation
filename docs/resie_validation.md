# Validation

In this section, the validation of single components of ReSiE is described. A validation of further detailed components and of whole energy systems will follow.

## Components
### Geothermal probe

The implementation of the model of the geothermal probes, as described in the [corresponding chapter](resie_energy_system_components.md#geothermal-probes), has been validated against measurement data and the commercial, widely used software Energy Earth Designer (EED) that uses a similar approach with g-functions as the model in ReSiE does. 
As measurement data, the project "GEW" in Gelsenkirchen, Germany was used. The monitoring project is described in detail in the publication Bockelmann2021[^Bockelmann2021]. Here, a probe field with 36 probes is investigated, including regeneration of the geothermal probe field using a reversible heat pump. For the validation presented here, the energies into and out of the probe field of the year 2014 were taken as inputs in EED and ReSiE, and the resulting average fluid temperature within the probe field was compared.

[^Bockelmann2021]: Bockelmann, Franziska: IEA HPT Annex 52 - Long-term performance monitoring of GSHP systems for commercial, institutional and multi-family buildings: Case study report for GEW, Germany, 2021, Braunschweig. doi:[https://doi.org/10.23697/0cfw-xw78](https://doi.org/10.23697/0cfw-xw78)

The 36 probes of the irregular shaped probe field were approximated using a rectangle shape with 3 x 12 probes with a distance of 8 m each in ReSiE, as there are no double-row L-configurations available as they are in EED, which would fit best to the original shape of the probe field. The g-function for this probe field was taken from the open source library by Spitler and Cook[^Spitler,Cook]. The thermal properties of the soil are known from a thermal response test at the site. 

[^Spitler,Cook]: J. D. Spitler, J. C. Cook, T. West, and X. Liu:  G-Function Library for Modeling Vertical Bore Ground Heat Exchanger. Geothermal Data Repository, 2021. doi: [https://doi.org/10.15121/1811518](https://doi.org/10.15121/1811518).

The results showed a high sensibility to the soil parameters and the thermal borehole resistance (or the parameters required to calculate it). The different probe field configuration in EED, a double L-configuration, compared to a rectangle in ReSiE, has almost no effect on the results.
The undisturbed ground temperature and also the temperature spread, that is assumed for the energy loading and unloading of the probe field, are also quite sensitive to the resulting average fluid temperature in the detailed model in ReSiE, as this directly affects the velocity of the fluid in the pipes and therefore the thermal resistance of the borehole. In the case study investigated, the power of the regeneration was much higher than the power of heat extraction, and therefore the temperature spread of loading had to be adjusted to meet the reality. The maximal output and input power was set very high to not limit the external energy sink and source into and out of the probe field. The thermal borehole resistance was calculated with the detailed model in ReSiE, but the simplified model with a constant thermal borehole resistance of \(0.1~W/(Km)\) shows also very good results in the comparison given the highly reduced amount of required input parameters.

For a better overview, the daily averaged mean temperature within the probe field is compared betweeen ReSiE (both simplified and detailed model), EED and the measurement data in the figure below. In the following table, the mean and the maximum absolute temperature differences are given, calculated for a timestep of one hour. Below, a line plot is comparing the daily averaged temperature of all four variants for an exemplary week.

| compared variants                   | mean abs. temp. diff. [K] | max. abs. temp. diff. [K] |
| ----------------------------------- | ------------------------- | ------------------------- | 
| ReSiE (detailed) vs. Measurement    | 0.47                      |  6.24                     |
| ReSiE (detailed) vs. EED            | 0.22                      |  1.41                     |
| ReSiE (simplified) vs. Measurement  | 0.44                      |  6.24                     |
| ReSiE (simplified) vs. EED          | 0.40                      |  1.97                     |

![Validation of probe model with measurement data and EED: Average fluid temperature daily](fig/240402_probe_compare_EED_Measurement_ReSiE_GEW2014_daily.svg)

Here, one week of the figure above is plotted with a higher temporal resolution of one hour, showing the high level of agreement between the results of ReSiE, EED and the measurement data:

![Validation of probe model with measurement data and EED: Average fluid temperature hourly](fig/240402_probe_compare_EED_Measurement_ReSiE_GEW2014_hourly.svg)

Below, a simulation of 25 years between ReSiE and EED is compared. The energy input and output profiles used in the validation described above are repeated for all 25 years. As the energy for regeneration is nearly the same as for energy extraction from the probe field, there is not much of a change in the average probe field temperature within the 25 years simulated. The comparison shows slight differences in the long term behaviour of the probe field of EED compared to ReSiE. This deviation was not further investigated so far but the differences are assumed to be neglectable. They do not originate from the different probe field layout, as the use of a rectangle probe field in EED has nearly no effect on the results, even after 25 years of simulation. The mean absolute temperature difference over 25 years between EED and ReSiE detailed (one hour resolution) is \(0.35~K\) and the maximum deviation is \(1.68~K\).

![Validation of probe model with measurement data and EED: Average fluid temperature 25 years](fig/240402_probe_compare_EED_ReSiE_GEW2014_25years.svg)

The input parameter of the simulation above is given in the following table. The highlighted values differ between the models:

| Parameter and unit                      | Value ReSiE   | Value EED | Value reality |
| --------------------------------------- | -----------   | --------- | ------------- | 
| probe field geometry                    | **3x12 rectangle**| **"10x10 L2-conf."**  | 36 irregular L-shape |
| borehole spacing [m]                    | 8             | 8         | irregular, 8 m in average     |
| probe depth [m]                         | 150           | 150       | 150           |
| probe type [-]                          | double-U      | double-U  | double-U      |
| borehole diameter [m]                   | 0.16          | 0.16      | 0.16          |  
| shank spacing [m]                       | 0.1           | 0.1       | ?             |  
| grout heat conductivity [W/(Km)]        | 2.0           | 2.0       | ?             |  
| effective thermal resistance [(Km)/W]   | 0.1 / calculated | calculated | ?         |
| soil undisturbed ground temperature [°C]| **13**        | **13**    | 12            |
| soil heat conductivity [W/(Km)]         | 1.6           | 1.6       | 1.6 (from thermal response test) |
| soil density [kg/m^3]                   | 1800          | 1800      | ? (clay and silt) |
| soil specific heat capacity [J/(kgK)]   | 2400          | 2400      | 2400          |
| ground heat capacity [MJ/(m^3/K)]       | -             | 4.32      | ?             |        
| pipe diameter outer [m]                 | 0.032         | 0.032     | 0.0320        |
| pipe diameter inner [m]                 | 0.0262        | 0.0262    | 0.0262        |
| pipe heat conductivity [W/(Km)]         | 0.42          | 0.42      | ?             |
| fluid specific heat capacity [J/(kgK)]  | 3795          | 3795      | 3795          |
| fluid density [kg/m^3]                  | 1052          | 1052      | 1052          |
| fluid kinematic viscosity [m^2/s]       | 3.9e-6        | -         | ?             |
| fluid dynamic viscosity [Kg/(ms)]       | -             | 4.103e-3  | ?             |
| fluid heat conductivity [W/(Km)]        | 0.48          | 0.48      | 0.48          |
| fluid prandtl number [-]                | 31.3          | ?         | 31.3          |
| borehole wall start temperature [°C]    | 13            | 13        | ?             |
| unloading temperature spread [K]        | **1.5**       | -         | 0.62 in average |
| loading temperature spread [K]          | **4.0**       | -         | 1.22 in average |

The profile of the input (regeneratrion) and output (heating) energy of the probe field (Wh in 15 min resolution) as well as the input and result files of EED and ReSiE (average fluid temperature, hourly resolution, in °C) can be downloaded [here](data/validation_probe.zip).

Also, a simulation performed with different time steps has been compared, from 15 minutes to 4 hours, showing only slight and expected differences in the average fluid temperature, caused by the different time resolution.

