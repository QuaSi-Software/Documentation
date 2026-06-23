# What is SoDeLe?

SoDeLe is a photovoltaic simulation tool within the QuaSi software environment. The name is an acronym for the German phrase *Solarsimulation denkbar leicht*, which can be translated as *solar simulation made easy*.

SoDeLe calculates PV yield profiles from weather data, module data, inverter assumptions, and the geometric orientation of one or more PV systems. It is intended for energy-system studies, district simulations, and early-stage planning tasks where reproducible PV time series are required but a full commercial PV design workflow is not necessary.

The calculation core is based on the Python library pvlib[^pvlib_python]. SoDeLe adds a practical workflow around pvlib: Excel-based input files, support for EPW and DWD weather files, access to module and inverter databases, and structured result files.


[^pvlib_python]: Holmgren et al., (2018). pvlib python: a python package for modeling solar energy systems. Journal of Open Source Software, 3(29), 884, [https://doi.org/10.21105/joss.00884](https://doi.org/10.21105/joss.00884)

## Purpose and scope

A PV system in SoDeLe is described by its orientation, tilt, module type, inverter model or constant inverter efficiency, electrical configuration, and weather file. The main output is a PV energy time series. Additional outputs contain annual yield values, area-specific and peak-power-specific values, aggregated results for several PV systems, and plots.

Typical applications are:

- generating annual PV production profiles for energy-system simulations,
- comparing PV orientations, tilts, or module layouts,
- preparing PV input profiles for district-level studies,
- estimating PV yield in early project phases,
- running scripted simulations from JSON input files.

SoDeLe is not a detailed PV plant design tool. It does not replace string-layout verification, shading analysis, mounting-system design, grid-connection planning, or project-specific engineering checks.

## User interfaces

SoDeLe can be used in three ways:

1. with the simplified Excel interface,
2. with the extended Excel interface,
3. from the command line with a JSON input file, either through the precompiled `SoDeLe.exe` or through the Python source code.

The Excel interfaces and the executable are intended for users without a Python installation. The command-line and Python workflows are intended for power users, automated workflows, and reproducible studies.

Both Excel interfaces use the same calculation core:

| Interface | Intended use |
| --------- | ------------ |
| `Sodele_Input_DE_simplified.xlsm` | Fast PV yield estimation with reduced input requirements and a constant DC-to-AC efficiency. |
| `Sodele_Input_DE_extended.xlsm` | Detailed PV system definitions with specific module and inverter selection and explicit electrical configuration. |

The files are available in the SoDeLe repository in the folder
[precompiled_with_frontend](https://github.com/QuaSi-Software/SoDeLe/tree/ea229027f8c847fac6cacc68c60aaec3ba54606d/precompiled_with_frontend).


This folder also contains the precompiled `SoDeLe.exe` and the required `src` folder with database resources. The Excel interfaces are currently provided in German and require Microsoft Excel with macro support on Windows.

## Data basis and limitations

SoDeLe supports EnergyPlus weather files (`.epw`) and DWD weather files (`.dat`) from the German Weather Service climate consulting module, available [here](https://kunden.dwd.de/obt/). Weather files are preprocessed internally before the pvlib calculation is performed, including time-stamp handling and, for DWD files, calculation of direct normal irradiance.

PV module and inverter parameters are read from public pvlib-compatible databases, including the CEC database from the [System Advisor Model (SAM) by NREL](https://github.com/NREL/SAM/tree/develop/deploy/libraries) and data provided with [pvlib](https://github.com/pvlib/pvlib-python/tree/main/pvlib/data).  For scripted workflows, the internal database names must be used exactly.

Relevant modelling limitations are:

- shading is not modelled,
- the simulation time step is determined by the weather file, typically one hour,
- result quality depends on the weather file, module entry, inverter entry, and electrical configuration,
- facade-mounted PV systems can be sensitive to weather-data conventions and diffuse-radiation assumptions (applies to all PV simulation tools).

Detailed instructions are provided in the [SoDeLe User Manual](sodele_user_manual.md).
