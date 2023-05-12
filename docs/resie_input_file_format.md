# Input file format

The required inputs to the simulation engine are given in the form a project file, which encodes the parameters in `JSON` format. Certain data, specifically large time series data, is offloaded into separate files in a CSV-like format and then referenced in the project file. The simulation engine can then be invoked by pointing to the project file. This means that the command-line interface has relatively few parameters and arguments are mostly put inside the project file. This file format and its expected content is described in detail in this chapter.

## Conventions

There are a few common issues that the file format itself cannot address. The conventions listed here have been established through the use of the input file format and can be considered part of it, but can also be ignored if needs be.

### Comments

The `JSON` format does not define comments. If there is a need to provide additional information to the reader inside the project file, or more commonly if alternative parameter values should be listed along the actual values, there is the option to add a parameter next to which element you want to comment on. Parameters with unknown name are simply ignored by the simulation engine, thus their values can be used to contain the comment text. To distinguish these comment parameters from actual parameters, prefix their name with a double underscore `__`.

### User address code

The units / energy system components in the project need to be addressed somehow as the connections work with these addresses as IDs. While the only requirement is that these User Address Codes (UAC) are unique, it makes sense to use an address system that provides additional information. This is especially useful if the results of the simulation are fed into BIM or monitoring software. Even if this is not the case, it still useful to use some kind of address system for easier debugging.

An example for a UAC system could be a hierarchical structure based on location and affiliation of the units within the buildings, encoded as segments and separated by an underscore. For example, `TST_A1_HVAC_01_BT` could reference a buffer tank used in the first HVAC cycle of the building "A1".

## Project file structure

The overall structure of the project file is split into three general sections, each of which is discussed in more detail below.

```json
{
    "io_settings": {...},
    "simulation_parameters": {...},
    "components": {...}
}
```

## Input / Output settings
```json
"io_settings": {
    "output_file": "./out.csv",
    "dump_info": true,
    "dump_info_file": "./info_dump.md",
    "output_keys": {
        "TST_01_HZG_01_CHP": ["m_h_w_ht1 OUT"],
        ...
    },
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

* `output_file` (`String`): File path to a location where the output will be saved.
* `dump_info` (`Boolean`): If true, will write additional information about the current run to a markdown file.
* `dump_info_file` (`String`): File path to where the additional information will be written.
* `output_keys` (`Map{String, List{String}}`): Specification for output file. See section on output specification (csv-file) for what this does and how it works.
* `output_plot` (`Map{Int, Dict{String, Any}`): Specification for output line plot. See section on output specification (interactive .html plot) for what this does and how it works.

### Output specification (csv-file)
```json
"output_keys": {
    "TST_01_HZG_01_CHP": ["m_h_w_ht1 OUT", "m_e_ac_230v OUT"],
    "TST_01_ELT_01_BAT": ["Load"],
    ...
}
```
The keys of this map must correspond exactly to the UAC of the components defined in the component specification. By the definition of a map, each component can only appear once in this map. If multiple outputs for a single component should be tracked, multiple entries should be put in the list mapped to that component's UAC. Each entry describes one input, output or other variable of that component. For example, `m_h_w_ht1 OUT` means that the output of medium `m_h_w_ht1` (hot water) of that component should be tracked.

The second part of the entry describes which of the available variables of the component the desired output is. For most components either `IN` (input) and/or `OUT` (output) is available, which additional variables depending on the type. For example, storage components often have the variable `Load` available, which corresponds to the amount of energy stored in the component. These additional variables do not have a medium associated with them and hence should be declared with their name alone.

### Output specification (interactive .html plot)
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
The output specification for an interactive line plot can be specified in ```"output_plot"```. The name of each object of this entry is a consecutive number starting from 1. Each value is a list of objects containing the fields ```"key"``` that has to match the UAC-name of the component and the medium of the requested data, ```"axis"``` that can be either "left" or "right" to choose on which y-axis the data should be plotted, ```"unit"``` as string displayed in the label of the output and ```"scale_factor"``` to scale the output data. Differing from ```"output_keys"```, here every output UAC has to be set as individual entry. Compare also to the example given above that displays the input and output thermal energy of one heat pump. Note that ```"unit"``` refers to the scaled data! 

The results will be saved in ```\output\output_plot.html"```. The plot can be opened with any browser and offers some possibilities of interactivity like zooming or hiding single data series.


## Simulation parameters
```json
"simulation_parameters": {
    "start": 0,
    "end": 604800,
    "time_step_seconds": 900
},
```

* `start` (`Integer`): Start time of the simulation in seconds.
* `end` (`Integer`): End time (inclusive) of the simulation in seconds.
* `time_step_seconds` (`Integer`): Time step in seconds.

**A note on time:** The simulation engine works entirely with timestamps relative to an arbitrary reference point. It is up to the user to choose these so that the simulation works well with the given inputs. The reference point can be the same as with the unix timestamp (1970-01-01 00:00:00) or it can be any number whatsoever as long as it is used consistently. The most important point is that the profiles used in the simulation match the reference point being used in the simulation parameters.

## Components

The specification for the components involved in the simulation is the most complicated part of the input file. Some of the parameters and values being used relate to the simulation model underlying the simulation engine. If you need to write this part of the input file from scratch, it is advised to read the chapter on the simulation model first, as this chapter only discusses the structure but not the meaning of the specification.

```json
"components": {
    "TST_01_HZG_01_CHP": {
        "type": "CHPP",
        "control_refs": ["TST_01_HZG_01_BFT"],
        "output_refs": [
            "TST_01_HZG_01_BUS",
            "TST_01_ELT_01_BUS"
        ],
        "strategy": {
            "name": "storage_driven",
            "high_threshold": 0.9,
            "low_threshold": 0.2
        },
        "power": 12500,
        "m_heat_out": "m_h_w_ht1"
    },
    "TST_01_HZG_01_BUS": {
        "type": "Bus",
        "medium": "m_h_w_ht1",
        "control_refs": [],
        "output_refs": [
            "TST_01_HZG_01_DEM",
            "TST_01_HZG_01_BFT"
        ],
        "input_priorities": [
            "TST_01_HZG_01_CHP",
            "TST_01_HZG_01_HTP",
            "TST_01_HZG_01_BFT"
        ],
        "connection_matrix": {
            "input_order": [
                "TST_01_HZG_01_CHP",
                "TST_01_HZG_01_HTP",
                "TST_01_HZG_01_BFT"
            ],
            "output_order": [
                "TST_01_HZG_01_DEM",
                "TST_01_HZG_01_BFT"
            ],
            "storage_loading": [
                [1, 0],
                [1, 1],
                [1, 0]
            ]
        }
    },
    ...
}
```

The specification is a map mapping a unit's UAC to the parameters required for initialization of that component. Parameters specific to the type of the component can be found in the chapter on the various types. In the following we discuss the parameters common to most or all types.

* `type` (`String`): The exact name of the type of the component.
* `medium` (`String`): Some components can be used for a number of different media, for example a bus or a storage. If that is the case, this entry must match exactly one of the medium codes used in the energy system (see also chapter on the simulation model).
* `control_refs` (`List{String}`): A list of UACs of units that are required for performing control calculations.
* `output_refs` (`List{String}`): A list of UACs of other units to which the unit outputs. Assignment of medium to component is given implicitly, as a component cannot output to two different components of the same medium.
* `strategy` (`String`): Parameters for the operation strategy of the component. Specific parameters depend on implementation and can be found in the chapter on the simulation model. The `strategy` entry can be omitted from the component entry, in which case a default strategy is used. If it is given, must contain at least the entry `name`, which must match exactly the internal name of a strategy.
* `input_priorities` (`List{String}`, Busses only): Bus components implement an input priority, meaning that the order in which energy is drawn from the other components connected to the bus can be customized to control energy flow in accordance to an operation strategy. The given list should be a list of the UACs of the connected components.
* `connection_matrix` (`List{String{Any}}`, Busses only): For busses, the connection matrix defines the input- and output order of the interconnected components. Currently, this is a doubling with `input_priorities` that will be resolved in future versions. The corresponding `storage_loading` matrix (rows are input_priorities, columns are output_priorities) can be given as matrix containing only 1 (true) or 0 (false). 1 means, a connection from input to output is allowed while 0 denys a connection from input to output. Note: This is currently only implemented if the output is a storage! If the output is an other component, the matrix will be ignored! The `storage_loading` matrix can be used to deny certain transformers to load a certain storage if they are connected to the same bus. The following figure illustrates the principle of the `storage_loading` matrix on the basis of the code example given above, where storage-loading is only allowed by the heat pump:
![Storage Loading Matrix](fig/230328_Storage_Loading_Matrix.svg)
* `m_heat_in`, `m_heat_out`, `m_gas_in`, `m_h2_out`, `m_o2_out`, `m_el_in`, `m_el_out` are optional. If they are provided within the set of parameters of a component, the default medium type is overwritten. This may can be useful as e.g. the electrolyser default waste heat output is of type `m_h_w_lt1` and can therefore not be fed into a bus with medium `m_h_w_ht1`. To change this, a user defined entry in the input file for `m_heat_out: "m_h_w_ht1"` can be given. Note: The user-defined medium name has to match exactly the required medium name of the interconnected component. As alternative, all media names can be set user-defined.

## Order of operation

The order of operation is usually calculated by a heuristic according to the control strategies defined in the input file and the interconnection of all components. This should usually work well and result in a correct order of operation which is then executed at each time step. The calculated operating sequence can be exported as a text file using the `dump_info` flag and the `dump_info_file` path in the `io_settings` section described above. In some cases, a custom order of operations may be required or desired. This can be done using the `order_of_operation` section in the input file. If this section is not specified or if it is empty, the order of operations will be calculated internally. If this section is not empty, the specified list will be read in and used as the calculation order. Note that the order of operations has a great influence on the simulation result and should be changed only by experienced users!
It may be convenient to first export the `dump_info` without a specification in `order_of_operation` to first calculate the default order or operation. The text provided in the exported `dump_info_file` can then be copied into `order_of_operation` in the input file and can be customized. The `order_of_operation` has to be a vector of strings each containing the UAC of a component and the desired operation step, separated by a whitespace. The UAC has to match exactly one of the UACs of the components defined in the section `components`. For a further description of the available operation steps, see section `Simulation sequence` in chapter `Fundamentals`. 

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
* `is_power` (`Boolean`): If true, the data is considered to be power values as an average over the timespan each time step covers. If false, the data is considered as the work done over the time step. Values that don't fit into a power/work pattern can be listed as power, as this means the values are not modified and read as-is.

### Time series data

Following the metadata block, the time series data is listed with one `timestamp` and `value` pair per line, separated by semicolon `;`. The number value should use a point `.` as the decimal separator. The timestamp should be listed as seconds relative to the reference point used throughout the simulation.
