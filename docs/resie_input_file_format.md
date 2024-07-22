# Input file format

The required inputs to the simulation engine are given in the form a project file, which encodes the parameters in `JSON` format. Certain data, specifically large time series data, is offloaded into separate files in a CSV-like format and then referenced in the project file. The simulation engine can then be invoked by pointing to the project file. This means that the command-line interface has relatively few parameters and arguments are mostly put inside the project file. This file format and its expected content is described in detail in this chapter.

## Conventions

There are a few common issues that the file format itself cannot address. The conventions listed here have been established through the use of the input file format and can be considered part of it, but can also be ignored if needs be.

### Comments

The `JSON` format does not define comments. If there is a need to provide additional information to the reader inside the project file, or more commonly if alternative parameter values should be listed along the actual values, there is the option to add a parameter next to which element you want to comment on. Parameters with unknown name are simply ignored by the simulation engine, thus their values can be used to contain the comment text. To distinguish these comment parameters from actual parameters, prefix their name with a double underscore `__`.

### User address code

The energy system components in the project need to be addressed somehow as the connections work with these addresses as IDs. While the only requirement is that these User Address Codes (UAC) are unique, it makes sense to use an address system that provides additional information and is understandable by humans. This is especially useful if the results of the simulation are fed into BIM or monitoring software. Even if this is not the case, it still useful to use some kind of address system for easier debugging.

An example for a UAC system could be a hierarchical structure based on location and affiliation of the components within the buildings, encoded as segments and separated by an underscore. For example, `TST_A1_HVAC_01_BT` could reference a buffer tank (`BT`) used in the first (`01`) `HVAC` cycle of the building `A1` in a project with prefix `TST`.

### Energy media

The specification of components and outputs often mention a medium, such as `m_h_w_ht1 OUT` to specifiy a high temperature heat output of some component. You can find a full explanation of what media are in the context of ReSiE [in the chapter on energy systems](resie_energy_systems.md#energy-media). We encourage the use of this naming structure, but this is not strictly necessary.

## Project file structure

The overall structure of the project file is split into three general sections and one specific one, each of which is discussed in more detail in the following sections.

```json
{
    "io_settings": {...},
    "simulation_parameters": {...},
    "components": {...},
    "order_of_operation": {...}
}
```

## Input / Output settings
```json
"io_settings": {
    "auxiliary_info": true,
    "auxiliary_info_file": "./auxiliary_info.md",
    "auxiliary_plots": true,
    "auxiliary_plots_path": "./output",
    "auxiliary_plots_formats": ["png", "svg"],
    "sankey_plot_file": "./output/output_sankey.html",
    "sankey_plot": "default",
    "csv_output_file": "./output/out.csv",
    "csv_output_keys": {
        "TST_01_HZG_01_CHP": ["m_h_w_ht1 OUT"],
        ...
    },
    "output_plot_file": "./output/output_plot.html",
	"output_plot": {
		"1": {
			"key": {"TST_01_HZG_01_CHP": ["m_h_w_ht1 OUT"]},
			"axis": "left",
			"unit": "kW",
			"scale_factor": 0.001
		},
		...
	}
},
```

* `csv_output_file` (`String`): (Optional) File path to where the CSV output will be written. Defaults to `./output/out.csv`.
* `csv_output_keys` (`Union{String, Dict{String, List{String}}}`): Specifications for CSV output file. See [section "Output specification (CSV-file)"](resie_input_file_format.md#output-specification-csv-file) for details.
* `auxiliary_info` (`Boolean`): If true, will write additional information about the current run to a markdown file.
* `auxiliary_info_file` (`String`): (Optional) File path to where the additional information will be written. Defaults to `./output/auxiliary_info.md`.
* `auxiliary_plots` (`Boolean`): If true, ReSiE will create additional plots of components, if available (currently only available for geothermal probe). Defaults to `false`.
* `auxiliary_plots_path` (`String`): (Optional) File path to where the additional plots will be saved. Defaults to `./output/`.
* `auxiliary_plots_formats` (`Arrax{String}`): Array of file formats that should be created. Can be one or multiple of `["html", "pdf", "png", "ps", "svg"]`.
* `sankey_plot_file` (`String`): (Optional) File path to where the Sankey plot will be written. Defaults to `./output/output_sankey.html`.
* `sankey_plot` (`Union{String, Dict{String, String}`): Specifications for sankey plot. See [section "Output specification (Sankey)"](resie_input_file_format.md#output-specification-sankey) for details.
* `output_plot_file`: (Optional) File path to where the output line plot will be written. Defaults to `./output/output_plot.html`.
* `output_plot` (`Union{String, Dict{Int, Dict{String, Any}}`): Specifications for output line plot. See [section "Output specification (interactive .html plot)"](resie_input_file_format.md#output-specification-interactive-html-plot) for details.

### Output specification (Sankey)

The energy system and the energy flows between its components can be displayed in a sankey plot. This plot shows not only the connections between all components but also the sums of energy transferred between them within in the simulation time span. This can be super helpful to check the overall functionality of the energy system, its structure and the overall energy balance.

In the `io_settings`, `sankey_plot` can be either ```"nothing"``` if no sankey should be created, ```"default"``` that creates a sankey plot with default colors or an array mapping all medium names used in the energy system to a color. This can be useful to better represent the various media, as the default colors may be confusing.
For a list of available named colors, refer to the [Julia Colors documentation](https://juliagraphics.github.io/Colors.jl/stable/namedcolors/). Note that the color for the medium "Losses" must be specified as well, even if it is not defined in the input file.

Below is an example of a custom color list for an energy system with three different media (plus "Losses"):
```json
 "sankey_plot": {
    "m_h_w_lt1": "indianred1",
    "m_h_w_ht1": "red",
    "m_e_ac_230v": "orange",
    "Losses": "black"
}
```					

The resulting plot will be saved by default in `./output/output_sankey.html`. The plot can be opened with any browser and offers some interactivity for the positions of elements.

### Output specification (CSV-file)

The output values of each component can be written to a CSV-file. `csv_output_keys` can either be ```"all"```, ```"nothing"``` or a list of entries as described below. For ```"csv_output_keys": "all"```, all possible output channels of all components will be written to the CSV-file, while for ```"nothing"``` no file will be created. 

To specify a custom selection of outputs, use the following syntax:

```json
"csv_output_keys": {
    "TST_01_HZG_01_CHP": ["m_h_w_ht1 OUT", "m_e_ac_230v OUT", "Losses"],
    "TST_01_ELT_01_BAT": ["Load"],
    ...
}
```
The keys of this map must correspond exactly to the UAC of the components defined in the component specification. By the definition of a map, each component can only appear once in this map. If multiple outputs for a single component should be tracked, multiple entries should be put in the list mapped to that component's UAC. Each entry describes one input, output or other variable of that component. For example, `m_h_w_ht1 OUT` means that the output of medium `m_h_w_ht1` (hot water) of that component should be tracked.

The second part of the entry describes which of the available variables of the component the desired output is. For most components either `IN` (input) and/or `OUT` (output) is available, which additional variables depending on the type. For example, storage components often have the variable `Load` available, which corresponds to the amount of energy stored in the component. Also, most of the transformer and storage components have the output variable `Losses`, which represents the total energy losses, while some components have an additional splitting into different media of the losses, like `Losses_heat` or `Losses_hydrogen`.  These additional variables do not have a medium associated with them and hence should be declared with their name alone. For details, which output channels are available for each component, see the [chapter on the component parameters](resie_component_parameters.md). 

### Output specification (interactive .html plot)

The output values of each component can be plotted in an interactive HTML-based line plot. `output_plot` can either be ```"all"```, ```"nothing"``` or a list of entries as described below. For ```"output_plot": "all"```, all possible output channels of all components will be plotted in the line plot, while for ```"nothing"``` no plot will be created. Note that for ```"output_plot": "all"```, the unit of each output is not specified as well as there is no `scale_factor` as for custon defined outputs. 

To define a custom plot, use the following syntax:

```json
"output_plot": {
    "1": {
        "key": {"TST_HP_01": ["m_h_w_lt1 IN"]},
        "axis": "left",
        "unit": "kW",
        "scale_factor": 0.001
    },
    "2": {
        "key": {"TST_HP_01": ["m_h_w_ht1 OUT"]},
        "axis": "left",
        "unit": "kW",
        "scale_factor": 0.001
    }
    ...
}
```
The name of each object of this entry is a consecutive number starting from 1. Each value is a list of objects containing the fields ```"key"``` that has to match the UAC-name of the component and the medium of the requested data, ```"axis"``` that can be either "left" or "right" to choose on which y-axis the data should be plotted, ```"unit"``` as string displayed in the label of the output and ```"scale_factor"``` to scale the output data. Differing from ```"csv_output_keys"```, here every output UAC has to be set as individual entry. Compare also to the example given above that displays the input and output thermal energy of one heat pump. Note that ```"unit"``` refers to the scaled data! 

The results will be saved by default in `./output/output_plot.html`. The plot can be opened with any browser and offers some interactivity like zooming or hiding data series.

## Simulation parameters
```json
"simulation_parameters": {
    "start": 0,
    "end": 604800,
    "time_step_seconds": 900,
    "weather_file_path": "./path/to/dat/or/epw/wather_file.epw",
},
```

* `start` (`Integer`): Start time of the simulation in seconds.
* `end` (`Integer`): End time (inclusive) of the simulation in seconds.
* `time_step_seconds` (`Integer`): Time step in seconds.
* `weather_file_path` (`String`): (Optional) File path to the project-wide weather file. Can either be an EnergyPlus Weather File (EPW, time step has to be one hour) or a .dat file from the DWD (see [https://kunden.dwd.de/obt/](https://kunden.dwd.de/obt/), free registration is required)

**A note on time:** The simulation engine works entirely with timestamps relative to an arbitrary reference point. It is up to the user to choose these so that the simulation works well with the given inputs. The reference point can be the same as with the unix timestamp (1970-01-01 00:00:00) or it can be any number whatsoever as long as it is used consistently. The most important point is that the profiles used in the simulation match the reference point being used in the simulation parameters.

## Components

The specification for the components involved in the simulation is the most complicated part of the input file. Some of the parameters and values being used relate to the simulation model underlying the simulation engine. If you need to write this part of the input file from scratch, it is advised to read the [chapters on the simulation model](resie_fundamentals.md) first, as this chapter only discusses the structure but not the meaning of the specification.

```json
"components": {
    "TST_01_HZG_01_CHP": {
        "type": "CHPP",
        "output_refs": [
            "TST_01_HZG_01_BUS",
            "TST_01_ELT_01_BUS"
        ],
        "control_parameters": {
            "load_storages m_e_ac_230v": false
        },
        "control_modules": [
            {
                "name": "storage_driven",
                "high_threshold": 0.9,
                "low_threshold": 0.2,
                "min_run_time": 3600,
                "storage_uac": "TST_01_HZG_01_BFT"
            }
        ],
        "power_el": 12500,
        "m_heat_out": "m_h_w_ht1"
    },
    "TST_01_HZG_01_BUS": {
        "type": "Bus",
        "medium": "m_h_w_ht1",
        "connections": {
            "input_order": [
                "TST_01_HZG_01_CHP",
                "TST_01_HZG_01_HTP",
                "TST_01_HZG_01_BFT"
            ],
            "output_order": [
                "TST_01_HZG_01_DEM",
                "TST_01_HZG_01_BFT"
            ],
            "energy_flow": [
                [1, 0],
                [1, 1],
                [1, 0]
            ]
        }
    },
    ...
}
```

The specification is a map mapping a component's UAC to the parameters required for initialization of that component. Parameters specific to the type of the component can be found in [the chapter on the various types](resie_component_parameters.md). In the following we discuss the parameters common to most or all types.

* `type` (`String`): The exact name of the type of the component.
* `medium` (`String`): Some components can be used for a number of different media, for example a bus or a storage. If that is the case, this entry must match exactly one of the medium codes used in the energy system (see also [this explanation](resie_energy_systems.md#energy-media)).
* `output_refs` (`List{String}`, non-Busses only): A list of UACs of other components to which the component outputs. Assignment of medium to component is given implicitly, as a component cannot output to two different components of the same medium.
* `control_parameters` (`Dict{String,Any}`): Parameters of the control and operational strategy of the component. See [this chapter](resie_operation_control.md) and [this section](resie_component_parameters.md#control-modules) for explanations. This entry can be omitted.
* `control_modules` (`List{Dict{String,Any}}`): List of control modules, where each entry holds the required parameters for that module. See [this chapter](resie_operation_control.md) and [this section](resie_component_parameters.md#control-modules) for explanations on control modules. This list can be omitted if no module is activated for the component.
* `m_heat_out` (`String`): The inputs and outputs of a component can be optionally configured with a chosen medium instead of the default value for the component's type. In this example the CHP's heat output has been configured to use medium `m_h_w_ht1`. The name has to match exactly one of the predefined media or a custom medium. Which parameter configures which input/output (e.g. `m_el_in` for electricity input) can be found in the [chapter on input specification of component parameters](resie_component_parameters.md).

The following parameter entries are for `Bus` components only:

* `connections` (`Dict{String, Any}`): Configuration of the connections of components over a bus. Sub-configs are:
    * `output_order` (`List{String}`): Similar to the entry `output_refs`, however the order of UACs in this list corresponds to the output priorities of components on the bus with entries at the beginning being given the highest priority and receiving energy first.
    * `input_order` (`List{String}`): Similar to the entry `output_order` but for the inputs on the bus.
    * `energy_flow` (`List{List{Int}}`): A matrix that defines which components are allowed to deliver energy to which other components. Rows correspond to the inputs and columns to outputs of the bus, both in the order defined in the entries `input_order` and `output_order`. The numbers should be 1 if the energy flow from the input (row) to the output (column) is allowed or 0 if it is not. No other numbers should be used. The following figure illustrates the principle of the `energy_flow` matrix on the basis of a bus with a CHP, a heat pump, a storage and a demand component. Only the heat pump is allowed to load the storage, while all three inputs (including storage) are allowed to deliver energy to the demand.
<center>![Storage Loading Matrix](fig/230328_Storage_Loading_Matrix.svg)</center>


## Order of operation

The order of operation is usually calculated by a heuristic according to the control strategies defined in the input file and the interconnection of all components. This should usually work well and result in a correct order of operation which is then executed at each time step. The calculated operating sequence can be exported as a text file using the `auxiliary_info` flag and the `auxiliary_info_file` path in the [Input/Output section](resie_input_file_format.md#input-output-settings) described above. In some cases, a custom order of operations may be required or desired. This can be done using the `order_of_operation` section in the input file. If this section is not specified or if it is empty, the order of operations will be calculated internally. If this section is not empty, the specified list will be read in and used as the calculation order. Note that the order of operations has a great influence on the simulation result and should be changed only by experienced users!

It may be convenient to first export the `auxiliary_info` without a specification in `order_of_operation` to first calculate the default order or operation. The text provided in the exported `auxiliary_info_file` can then be copied into `order_of_operation` in the input file and can be customized. The `order_of_operation` has to be a vector of strings each containing the UAC of a component and the desired operation step, separated by a whitespace. The UAC has to match exactly one of the UACs of the components defined in the section `components`. For a further description of the available operation steps, see [this section on the simulation sequence](resie_fundamentals.md#determining-order-of-operations).

Example of a generated order of operation:
```json
"order_of_operation": [
    "TST_DEM_01 s_reset",
    "TST_HP_01 s_reset",
    "TST_SRC_01 s_reset",
    "TST_GRI_01 s_reset",
    "TST_DEM_01 s_control",
    "TST_HP_01 s_control",
    "TST_SRC_01 s_control",
    "TST_GRI_01 s_control",
    "TST_DEM_01 s_process",
    "TST_HP_01 s_process",
    "TST_SRC_01 s_process",
    "TST_GRI_01 s_process"
]
```


## Profile file format

As discussed earlier, time series data is separated into its own file format so as to not clutter the project file and turn it unreadable. This profile file format resembles a `CSV` format with a few additions.

```csv
# time_step;900
# is_power;false
0;0.05
900;0.15
1800;0.1
...
```

### Metadata

Instead of a header row, there is a block of metadata describing important information on the time series data. The metadata is given as comment lines (starting the line with `#`) of `name;value` pairs. Some specific metadata is expected, as described in the following, but any kind of metadata can be added to provide additional information.

* `time_step` (`Integer`): The time step, in seconds, used by the time series.
* `is_power` (`Boolean`): If true, the data is considered to be power values as an average over the timespan each time step covers. If false, the data is considered as the work done over the time step. Values that don't fit into a power/work pattern, like temperatures or operation states,  **must** be listed as `is_power;true`, as this means the values are not modified and read as-is.

### Time series data

Following the metadata block, the time series data is listed with one `timestamp` and `value` pair per line, separated by semicolon `;`. The number value should use a point `.` as the decimal separator. The timestamp should be listed as seconds relative to the reference point used throughout the simulation.

### Time step width

ReSiE automatically converts the time series data of the profiles to the time step of the simulation, specified at `simulation_parameters": "time_step_seconds":`. Aggregation as well as segmentation of intensive (`is_power;true` for e.g. temperatures) and extensive values (`is_power;false` for e.g. energies) can be performed. Segmentation of intensive values is done using linear interpolation between the original time steps. During segmentation of extensive values instead, ReSiE divides the original value evenly among the smaller intervals. This means, each smaller time segment within a larger one receives the same value, effectively spreading the original value evenly over the time it covers. With extensive aggregation, the sum of the original values that compose the new time step is calculated, while with intensive values, the mean of the original values is taken to obtain the corresponding value of the new profile.

Please note that currently only exact dividers or multiples of the time steps of the simulation and the profiles can be handled by the algorithm (e.g. 60 min --> 15 min or 15 min --> 30 min). Otherwise an error will arise, like for 15 min --> 6 min or 15 min --> 20 min.