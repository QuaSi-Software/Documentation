# SoDeLe User Manual

This manual describes how to run SoDeLe with the Excel interfaces and how to use the command-line/JSON workflow. For the general concept and modelling scope, see [What is SoDeLe?](sodele_overview.md).

## Use SoDeLe with Excel

For use **without** a Python installation, download or clone the [SoDeLe repository](https://github.com/QuaSi-Software/SoDeLe/tree/main) and use the folder:

```text
precompiled_with_frontend
```

Keep the contents of this folder together. In particular, `SoDeLe.exe` and the `src` folder must remain in the same directory, because the executable expects the PV module and inverter resources below `src/sodele/res/PV_Database/`. For best performance, copy the complete folder to a local directory before starting a simulation.

The folder contains two Excel interfaces:

- `Sodele_Input_DE_simplified.xlsm`: Simplified input for fast PV yield estimation. It uses a reduced module selection and a constant DC-to-AC efficiency instead of detailed inverter modelling.
- `Sodele_Input_DE_extended.xlsm`: Extended input for experienced users. It allows specific module and inverter selection, module string configuration, number of inverters, and optional use of a constant inverter efficiency.

The Excel interfaces are currently provided in German and require Microsoft Excel with macro support on Windows. Excel 2016 and Excel 365 are tested. If macros are blocked after downloading, unblock the `.xlsm` file in the Windows file properties and then enable macros in Excel.

Basic workflow:

1. Open either the simplified or the extended Excel interface.
2. Enable macros.
3. Select an `.epw` or DWD `.dat` weather file with the browse button.
4. Enter orientation, tilt, module quantity, module type, inverter assumptions, and output settings.
5. Start the simulation with the Excel button. Note that this can take some time at the first time.
6. Check the console output for the selected weather file and location.
7. Use the generated result folder for time series, key values, and plots.

Do not add or delete cells in the Excel files and do not rename worksheets. The VBA interface expects the workbook structure to remain unchanged. If interactive plots are shown, close the plot windows to complete the result-writing process.

## Use SoDeLe via command-line and JSON input file

The 'SoDeLe.exe' can also be accessed using a command-line interface. The relevant command for simulations is `simulatePv`.

Run the executable from the `precompiled_with_frontend` folderfrom a command line:

```bash
cd path/to/precompiled_with_frontend
SoDeLe.exe simulatePv -i path/to/input.json
```

The `-i` argument can also be written as `--input_json`. Relative paths inside the JSON file, including `weatherData.weatherDataFile`, are resolved against the current working directory from which the command is executed, not against the JSON file location.

A representative input file for local weather-file based simulations is shown below. Additional PV systems can be added as further objects in the `PhotovoltaicPlants` array.

```json
{
  "PhotovoltaicPlants": [
    {
      "surfaceAzimuth": 180,
      "surfaceTilt": 30,
      "modulesPerString": 23,
      "stringsPerInverter": 1,
      "numberOfInverters": 5,
      "albedo": 0.2,
      "moduleInstallation": 1,
      "modulesDatabaseType": 1,
      "moduleName": "Aleo_S16_180__2007__E__",
      "inverterName": "Auxin_Solar__AXN_PV4000U__208V_",
      "useStandByPowerInverter": true,
      "useInverterDatabase": true,
      "inverterEta": 0.92,
      "lossesIrradiation": 1,
      "lossesDCDatasheet": 2,
      "lossesDCCables": 0
    }
  ],
  "weatherData": {
    "latitude": 0,
    "longitude": 0,
    "weatherDataFile": "./Wetter/TRY2015_Stuttgart_JahrEPW.epw"
  },
  "showPlots": false
}
```

For Windows paths in JSON, either use forward slashes or escape backslashes, for example `"C:\\path\\to\\weather.epw"`.

### Input parameters

The column `R/D` indicates whether a parameter is required and whether a default value is provided by the code. `R/N` means required with no default. `N/D` means optional with a code default. `N/N` means optional without a relevant public-workflow default.

Top-level and weather-data parameters:

| Name | Type | R/D | Example | Unit | Description |
| ---- | ---- | --- | ------- | ---- | ----------- |
| `PhotovoltaicPlants` | `Array{Object}` | R/N | `[{...}]` | [-] | Define one or more PV systems to simulate. |
| `weatherData` | `Object` | R/N | `{...}` | [-] | Define the weather input. For public use, provide `weatherDataFile` inside this object. |
| `weatherDataFile` | `String` | R/N | `"./Wetter/TRY2015_Stuttgart_JahrEPW.epw"` | [-] | Path to a local `.epw` or DWD `.dat` weather file. Relative paths are resolved against the current working directory. |
| `latitude` | `Float` | N/N | `0` | [°] | Placeholder used by Excel-generated files and by environment-specific remote weather-data workflows. Not required when `weatherDataFile` is used. |
| `longitude` | `Float` | N/N | `0` | [°] | Placeholder used by Excel-generated files and by environment-specific remote weather-data workflows. Not required when `weatherDataFile` is used. |
| `showPlots` | `Boolean` | N/D | `false` | [-] | Set whether plots are shown interactively after the simulation. |
| `keep_files` | `Boolean` | N/D | `false` | [-] | Set whether temporary files should be kept or deleteted afer the simulation. |
| `uuid` | `String` | N/D | Automatically generated | [-] | Optional simulation identifier. |

Parameters for each object in `PhotovoltaicPlants`:

| Name | Type | R/D | Example | Unit | Description |
| ---- | ---- | --- | ------- | ---- | ----------- |
| `uid` | `String` | N/D | Automatically generated | [-] | Optional unique identifier of the PV system. |
| `surfaceAzimuth` | `Float` | N/D | `180` | [°] | Azimuth angle of the modules; `0` = north, `90` = east, `180` = south, `270` = west. |
| `surfaceTilt` | `Float` | N/D | `30` | [°] | Tilt angle of the modules; `0` = horizontal, `90` = vertical. |
| `modulesPerString` | `Float` | N/D | `23` | [-] | Number of modules connected in series in one string. Can also be a float if `useInverterDatabase` is `false`. |
| `stringsPerInverter` | `Int` | N/D | `1` | [-] | Number of strings connected in parallel to one inverter. |
| `numberOfInverters` | `Int` | N/D | `5` | [-] | Number of identical inverters represented by this PV system. |
| `albedo` | `Float` | N/D | `0.2` | [-] | Ground-reflection coefficient of the surroundings. |
| `moduleInstallation` | `Int` | N/D | `1` | [-] | Encoded module installation type; see table below. |
| `modulesDatabaseType` | `Int` | N/D | `2` | [-] | Encoded PV module database type; see table below. |
| `moduleName` | `String` | R/N | `"Aavid_Solar_ASMS_165P"` | [-] | Internal name of the PV module in the selected module database. |
| `inverterName` | `String` | N/D | `"KACO__blueplanet_3601xi__240V_"` | [-] | Internal name of the inverter in the CEC inverter database. A valid name is required in practice, also when `useInverterDatabase` is `false`. |
| `useStandByPowerInverter` | `Boolean` | N/D | `false` | [-] | Set whether negative standby power of the inverter is retained. If `false`, negative AC power values are set to zero. |
| `useInverterDatabase` | `Boolean` | N/D | `true` | [-] | Set whether the inverter is modelled from the inverter database. If `false`, `inverterEta` is used as constant DC-to-AC efficiency and the string layout is not required. |
| `inverterEta` | `Float` | N/D | `0.92` | [-] | Constant DC-to-AC conversion efficiency used when `useInverterDatabase` is `false`. |
| `lossesIrradiation` | `Float` | N/D | `1` | [%] | Additional irradiation reduction applied to GHI, DNI, and DHI. |
| `lossesDCDatasheet` | `Float` | N/D | `2` | [%] | Additional DC-side losses within the PVWatts losses model. |
| `lossesDCCables` | `Float` | N/D | `0` | [%] | Ohmic DC cable losses relative to standard test conditions. |

Encoded values:

| Parameter | Value | Meaning |
| --------- | ----- | ------- |
| `moduleInstallation` | `1` | Open-rack installation with glass-glass module construction. |
| `moduleInstallation` | `2` | Open-rack installation with glass-polymer module construction. |
| `moduleInstallation` | `3` | Close-mount installation with glass-glass module construction. |
| `moduleInstallation` | `4` | Insulated-back installation with glass-polymer module construction. |
| `modulesDatabaseType` | `1` | Sandia module database with SAPM DC model. |
| `modulesDatabaseType` | `2` | CEC module database with CEC DC model. |

The inverter database is the CEC inverter database for both module database types. Module and inverter names must match the internal pvlib database names exactly. Valid names can be taken from the extended Excel interface or from the text files in `src/sodele/res/PV_Database/`.

The total number of modules represented by one PV-system object is:

$$
N_\mathrm{modules} = N_\mathrm{inv} \cdot N_\mathrm{strings/inv} \cdot N_\mathrm{modules/string}
$$

where \(N_\mathrm{inv}\) is `numberOfInverters`, \(N_\mathrm{strings/inv}\) is `stringsPerInverter`, and \(N_\mathrm{modules/string}\) is `modulesPerString`.

## Weather data and databases

SoDeLe supports two local weather-file types:

- `.epw`: EnergyPlus weather files,
- `.dat`: DWD weather files from the German Weather Service climate consulting module [available here](https://kunden.dwd.de/obt/index.jsp).

For EPW files, radiation values are interpreted as values for the previous time step. The internal time stamp is shifted by 30 minutes so that radiation data are assigned to the corresponding solar position. For DWD `.dat` files, direct normal irradiance is not provided directly and is calculated internally before the PV yield calculation.

The DWD `.dat` import expects the format of the DWD climate consulting module: 8760 hourly values, no leap year, GMT+1/CET without daylight-saving-time handling, first data point on January 1 at 01:00, and a measurement section beginning with `***`. Current and future test reference years can be used.

PV module and inverter parameters are based mainly on the CEC database from the [System Advisor Model (SAM) by NREL](https://github.com/NREL/SAM/tree/develop/deploy/libraries) and data provided with [pvlib](https://github.com/pvlib/pvlib-python/tree/main/pvlib/data).

To regenerate internal module and inverter name lists from CEC CSV files, use:

```bash
python bin/app.py generatePVDatabase -p path/to/database/folder
```

The folder passed via `-p` or `--path` must contain:

```text
CEC_Modules.csv
CEC_Inverters.csv
```

## Output and limitations

For `simulatePv`, the output folder is derived from the input JSON path:

```text
path/to/input_result/
```

The folder contains `result.json` and generated plot files. The JSON result contains individual results for each PV system and a summary over all systems.

| Name | Unit | Description |
| ---- | ---- | ----------- |
| `EnergyProfile` | [kWh] | Energy yield per time step. |
| `EnergyAreaProfile` | [kWh/m²] | Area-specific energy yield per time step. |
| `SumOfEnergyPerYear` | [kWh] | Sum of the energy yield over the simulated year. |
| `WorkSpecificEnergyPerYear` | [kWh/kWp] | Annual yield divided by installed peak power. |
| `AreaSpecificEnergyPerYear` | [kWh/m²] | Annual yield divided by PV module area. |

SoDeLe is intended for PV yield-profile generation, not detailed PV plant engineering. Shading is not modelled, the time step is limited by the weather file, and result quality depends on the selected weather data, module entry, inverter entry, and electrical configuration.

For facade PV and other sensitive cases, check the plausibility of the weather-data time-stamp convention, for example by comparing east- and west-facing vertical systems, especially if you use EPW files that are not strictly created following the [EPW file standard](https://designbuilder.co.uk/cahelp/Content/EnergyPlusWeatherFileFormat.htm).

## Running from Python

Running SoDeLe from Python is mainly useful for development, debugging, batch simulations, or workflows where a Python environment is already available. Compared to the SoDeLe.exe via CLI, directly accessing SoDeLe in Python is much faster.

```bash
cd path/to/local/sodele/repository
python bin/app.py simulatePv -i path/to/input.json
```

## Updating the module and inverter database

SoDeLe uses PV module and inverter data from established public databases. CEC module and inverter data can be obtained from the National Renewable Energy Laboratory's [System Advisor Model (SAM)](https://github.com/NREL/SAM/tree/develop/deploy/libraries). Sandia module data can be obtained from the [pvlib data repository](https://github.com/pvlib/pvlib-python/tree/main/pvlib/data).


To update the local module and inverter database:

1. Download the updated module and inverter database files from the selected source.
2. Check the CSV files for duplicate entries. Duplicate entries can cause errors when the data is loaded by pvlib.
3. Place the updated database files in the database directory used by SoDeLe.
4. Run the SoDeLe database-generation command to generate the text files with the internal module and inverter names:
   `  python bin/app.py generatePVDatabase --path path/to/database/folder`.
5. Update the hidden database sheets in the Excel input files with the generated internal names and the corresponding user-facing descriptions.
6. Check and, if necessary, extend the Excel formulas and dropdown ranges so that the full updated database is available in the input interface.
7. Run a small test simulation with representative module and inverter selections to verify that the updated database is read correctly.

The internal names used in the JSON input file must match the names generated from the database. This applies to both `moduleName` and `inverterName`. When the inverter database is not used and a constant inverter efficiency is specified instead, a valid inverter name is still required for compatibility with the pvlib workflow.

## Generating a new SoDeLe executable

A new executable can be generated from the Python source code with `PyInstaller`. This is mainly relevant when the SoDeLe source code or bundled resource files have changed and the Excel interface should use an updated standalone executable.

First, install the Python dependencies in the project environment. Then run the build script from the root directory of the SoDeLe repository:

```bash
python buildAsExe.py
```

The build script uses PyInstaller with the following main settings:

```python
PyInstaller.__main__.run([
    './bin/app.py',
    '-p', './src/',
    '--add-data', './src/sodele/;./src/sodele/',
    '--onefile',
])
```

This creates a single-file executable from `bin/app.py` and includes the required `src/sodele` resources in the bundled application. After the build has finished, the executable is written to the `dist` directory. Depending on the generated file name, rename the executable to `SoDeLe.exe` before using it with the Excel interface.

After generating the executable, test it from the command line with a known JSON input file:

```bash
SoDeLe.exe simulatePv -i path/to/input.json
```

For the Excel workflow, make sure that the updated `SoDeLe.exe` is located in the directory expected by the Excel input files and that all required resource files are available.

Please note that the CSV files containing the module and inverter databases must be added to the file structure, as PyInstaller does not integrate them properly.

## Validation

SoDeLe has been checked against established PV simulation tools to assess the plausibility of the calculated annual PV yields. The comparison included simulations with a detailed inverter model and simulations with a constant electrical DC-AC efficiency of 92 %. The annual energy yield was compared for one PV module, four different orientations, and four different locations.

For common roof-oriented PV systems, the deviation of the annual yield compared with the commercially available `PV*SOL`[^PVSOL] was below 5 %. For façade-oriented systems in east-west orientation, deviations of up to 15 % in extreme scenarios were observed compared with `PVGIS`[^PVGIS], while the results from `PV*SOL` remain close to the one of SoDeLe. The daily profiles showed small but visible differences.

The comparison should be interpreted as a tool-to-tool verification and plausibility check, not as a complete certification of the model. Differences mainly result from different irradiance-processing methods, different assumptions for diffuse radiation, and potentially non-identical module or inverter parameter sets in the compared databases.

[^PVSOL]: Valentin Software - PV*SOL premium: Design and simulation software for photovoltaic systems. Available [here](https://valentin-software.com/en/products/pvsol-premium/).

[^PVGIS]: European Commission Joint Research Centre - Photovoltaic Geographical Information System (PVGIS), available [here](https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html).