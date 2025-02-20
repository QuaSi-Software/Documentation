# Types of energy system components
This chapter provides details on the parameters of energy system components, which can be used in the [project input file](resie_input_file_format.md). For a detailed description of the mathematical models, see the [chapter on the component models](resie_energy_system_components.md).

The description of each component type includes a block with a number of attributes that describe the type and how it connects to other components by its input and output interfaces. An example of such a block:

| | |
| --- | --- |
| **Type name** | `BoundedSink`|
| **File** | `energy_systems/general/bounded_sink.jl` |
| **System function** | `bounded_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | |
| **Tracked values** | `IN`, `Max_Energy`, `Losses` |

Of particular note are the descriptions of the medium (if it applies) of the component type and its input and output interfaces. The `Medium` is used for components that could handle any type of medium and need to be configured to work with a specific medium. The attributes `Input media` and `Output media` describes which input and output interfaces the type provides and how the media of those can be configured. The syntax `name`/`value` lists the name of the parameter in the input data that defines the medium first, followed by a forward slash and the default value of the medium, if any. A value of `None` implies that no default is set and therefore it must be given in the input data. A value of `auto` implies that the value is determined with no required input, usually from the `Medium`.

The `Tracked values` attribute lists which values of the component can be tracked with the output specification in the input file (see [this section](resie_input_file_format.md#output-specification-csv-file) for details). Note that a value of `IN` or `OUT` refers to all input or output interfaces of the component. Which these are can be infered from the input and output media attributes and the chosen medium names if they differ from the default values.

The description further lists which arguments the implementation takes. Let's take a look at an example:

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `max_power_profile_file_path` | `String` | Y/N | `profiles/district/max_power.prf` | Path to the max power profile. |
| `efficiency` | `Float` | Y/Y | 0.8 | Ratio of output over input energies. |
| `constant_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the heat output to a constant value. |

The name of the entries should match the keys in the input file, which is carried verbatim as entries to the dictionary argument of the component's constructor. The column `R/D` lists if the argument is required (`R`) and if it has a default value (`D`). If the argument has a default value the example value given in the next column also lists what that default value is. Otherwise the example column shows what a value might look like.

The type refers to the type it is expected to have after being parsed by the JSON library. The type `Temperature` is an internal structure and simply refers to either `Float` or `Nothing`, the null-type in Julia. In general, a temperature of `Nothing` implies that any temperature is accepted and only the amount of energy is revelant. More restrictive number types are automatically cast to their superset, but *not* the other way around, e.g: \(UInt \rightarrow Int \rightarrow Float \rightarrow Temperature\). Dictionaries given in the `{"key":value}` notation in JSON are parsed as `Dict{String,Any}`.

### Storage un-/loading
All components can be set to be dis-/allowed to un-/load storages to which they output or from which they draw energy. This only makes sense if an intermediary bus exists because direct connections to/from storages must always be allowed to transfer energy. Here are exemplary parameters for a `BoundedSupply`:

```json
{
    "uac": "TST_SRC_01",
    "type": "BoundedSupply",
    "medium": "m_h_w_lt1",
    ...
    "control_parameters": {
        "load_storages m_h_w_lt1": false
    }
}
```

This would result in the output of the source not being used to fill storages. The name of the `load_storages medium` parameter must match the name of the medium of the input/output in question. The medium name `m_h_w_lt1` is, in this case, derived from the parameter `medium`. The medium name might also be set directly, for example with `m_heat_in` for a `HeatPump`.

Similarly, components can be configured to be dis-/allowed to draw energy from storages with the corresponding `unload_storages medium` parameter. Any input/output not specified in this way is assumed to be allowed to un-/load storages.

### Function definitions
Various components, particularly transformers, require an input of functions to determine efficiency, available power and other variables. The definition of a function in the project file is a string and should look like `function_prototype:values` with `function_prototype` refering to one of the implemented function prototypes (see specific sub-sections below) and `values` being data required to parameterise the prototype. Various function prototypes are implemented for different purposes.

In general `:` is used as seperator between prototype and values and `,` as seperator for numbers with `.` as decimal point and no thousands seperator.

#### Efficiency functions
Used to determine an efficiency factor of how much energy is produced from a given input and vice-versa. This is described in more detail in [the chapter on general effects and traits](resie_transient_effects.md#part-load-ratio-dependent-efficiency). In the simplest case this can be a constant factor, such as a 1:1 ratio, however in the mathematical models of the components this can be almost any continuous function mapping \(\kappa \in [0,1]\) to an efficiency factor.

Because the efficiency must always be defined in relation on input or output of the component, the functionality supports this interface being defined as linear. This means that the amount of energy on this interface is strictly linear to the PLR multiplied with the design power. The other interfaces of the component are then calculated with efficiencies relative to this linear interface. Example: A fuel boiler defined with linear heat output would have a constant efficiency of 1.0 on the heat output and a different efficiency on the fuel input. If the conversion from fuel to heat is 90% efficient, this results in an efficiency factor of 1.1 on the fuel input.

For the configuration of components a selected number of different cases are implemented. If a function is known, but cannot be precisely modelled using one of these parameterised functions, it is possible to use a piece-wise linear approximation, which is also useful to model data-driven functions.

**Implemented function prototypes**

* `const`: Takes one number and uses it as a constant efficiency factor. E.g. `const:0.9`.
* `poly`: Takes a list of numbers and uses them as the coefficients of a polynomial with order n-1 where n is the length of coefficients. The list starts with coefficients of the highest order. E.g. `poly:0.5,2.0,0.1` means \(e(x) = 0.5x^2 + 2x + 0.1\)
* `pwlin`: A piece-wise linear interpolation. Takes a list of numbers and uses them as support values for an even distribution of linear sections on the interval [0,1]. The PLR-values (on the x axis) are implicit with a step size equal to the inverse of the length of support values minus 1. The first and last support values are used as the values for a PLR of 0.0 and 1.0 respectively. E.g. `pwlin:0.6,0.8,0.9` means two sections of step size 0.5 with a value of `e(0.0)==0.6`, `e(0.5)==0.8`, `e(1.0)=0.9` and linear interpolation inbetween.
* `offset_lin`: Takes one number and uses as the slope of a linear function with an offset of its complement (in regards to 1.0). E.g. `offset_lin:0.5` means \(e(x)=1.0-0.5*(1.0-x)\)
* `logarithmic`: Takes two numbers and uses them as the coefficients of a quasi-logarithmic function. E.g. `logarithmic:0.5,0.3` means \(e(x)=\frac{0.5x}{0.3x+(1-0.3)}\)
* `inv_poly`: Takes a list of numbers and uses them as the coefficients of a polynomial with order n-1 where n is the length of coefficients. The list starts with coefficients of the highest order. The inverse of the polynomial, multiplied with the PLR, is used as the efficiency function. E.g. `inv_poly:0.5,2.0,0.1` means \(e(x)=\frac{x}{0.5x²+2x+0.1}\)
* `exp`: Takes three numbers and uses them as the coefficients of an exponential function. E.g. `exp:0.1,0.2,0.3` means \(e(x)=0.1+0.2*exp(0.3x)\)
* `unified_plf`: Takes four numbers and uses them as the coefficients of a composite function of a logarithmic and linear function as described in the documentation on the [unified formulation for PLR-dependent efficiencies of heat pumps](resie_energy_system_components.md#part-load-efficiency). The first two numbers are the optimal PLR and the PLF at that PLR. The third number is a scaling factor for the logarithmic part and the fourth number is the PLF at PLR=1.0.

**Discretization**

Because not all functions are (easily) invertible a numerical approximation of the inverse function is precalculated during initialisation. The size of the discretization step can be controlled with the parameter `nr_discretization_steps`, which has a default value of 30 steps. It should not often be necessary to use a different value, but this can be beneficial to balance accuracy vs. performance. In particular if a piece-wise linear interpolation is used it makes sense to use the same number of discretization steps so that the support values overlap for both the efficiency function and its inverse.

**PLF functions**

The calculation of some components, such as heat pumps, makes use of the part load factor (PLF), which is multiplied after an efficiency factor has been calculated from some other formulation and which represents the behaviour dependent on \(\kappa\). For parsing, these work the same as the efficiency functions, however they may not make use of the numerical approximation of the inverse function.

#### COP functions
Used by heat pumps and similar components to calculate the COP depending on input/output temperatures. The implemented function prototypes are two-dimensional functions that return the COP without considering additional modifications such as a PLF function or icing losses. The temperatures are assumed to be given in °C.

**Implemented function prototypes**

* `const`: Takes one number and uses it as a constant COP. E.g. `const:3.1`.
* `carnot`: Calculates the COP as fraction of the Carnot-COP with a given reduction factor, which is between `0.4` and `0.45` for typical heat pumps. E.g. `carnot:0.4` means \(COP = 0.4 \cdot \frac{273.15 + T_{out}}{T_{out} - T_{in}}\).
* `poly-2`: A 2D-polynomial of order three. Takes a list of ten values for the constants in \(f(x,y) = c_1 + c_2 \ x + c_3 \ y + c_4 \ x^2 + c_5 \ x \ y + c_6 \ y^2 + c_7 \ x^3 + c_8 \ x^2 \ y + c_9 \ x \ y^2 + c_{10} \ y^3\). E.g. `poly-2:0.3,0.4,0.1,0.2,0.0,0.0,0.0,0.0,0.0,0.0`.
* `field`: Two-dimensional field values with bi-linear interpolation between the support values. See explanation below for how the definition should be given. The minimal and maximal values are interpreted as the inclusive boundaries of the field. Values outside of the boundaries lead to errors and are not extrapolated. The support values should be equally spaced along the dimensions for numerical stability, although the interpolation algorithm does not check and works with varying spacing too.

An example of a field definition with additional line breaks and spaces added for clarity:
```
"field:
 0, 0,10,20,30;
 0,15, 9, 6, 4;
10,15,15,10, 7;
20,15,15,15,11"
```
The first row are the grid points along the \(T_{sink,out}\) dimension, with the first value being ignored. The points cover a range from 0 °C to 30 °C with a spacing of 10 K. The first column are the grid points along the \(T_{source,in}\) dimension, with the first value being ignored. The points cover a range from 0 °C to 20 °C with a spacing of 10 K. The support values are the COP (at maximum PLR \(\kappa = 1\)), for example a value of 10 for \(T_{source,in} = 10, \ T_{sink,out} = 20\).

#### Power functions
Used by heat pumps and similar components to calculate the minimum and maximum power available, depending on temperature values, as fraction of the nominal power. Return values should therefore be in \([0,1]\).

**Implemented function prototypes**

* `const`: Takes one number and uses it as a constant fraction. E.g. `const:1.0`.
* `poly-2`: A 2D-polynomial of order three. Takes a list of ten values for the constants in \(f(x,y) = c_1 + c_2 \ x + c_3 \ y + c_4 \ x^2 + c_5 \ x \ y + c_6 \ y^2 + c_7 \ x^3 + c_8 \ x^2 \ y + c_9 \ x \ y^2 + c_{10} \ y^3\). E.g. `poly-2:0.3,0.4,0.1,0.2,0.0,0.0,0.0,0.0,0.0,0.0`.


### Control modules
For a general overview of what control modules do and how they work, see [this chapter](resie_operation_control.md). In the following the currently implemented control modules and their required parameters are listed.

Some parameters specify behaviour of multiple modules on the same component as well as other control behaviour of the component. As the `control_modules` subconfig is a list and cannot hold parameters, these are specified in the `control_parameters` subconfig. In addition to [the storage un-/loading flags](resie_component_parameters.md) these general control parameters are:

| | |
| --- | --- |
| **aggregation_plr_limit** | How the upper PLR limit is aggregated. Should be either `max` (take the maximum) or `min` (take the minimum). Defaults to `max`. |
| **aggregation_charge** | How the charging flag is aggregated. Should be either `all` (all must be `true`) or `any` (any one must be `true`). Defaults to `all`. |
| **aggregation_discharge** | How the discharging flag is aggregated. Should be either `all` (all must be `true`) or `any` (any one must be `true`). Defaults to `all`. |

The aggregation defined in `aggregation_plr_limit` applies to the control modules `storage_driven` and `profile_limited` as they both use the PLR limit callback `upper_plr_limit`.

A definition of a control module with its control parameter can be done for example like this:

```JSON
"TST_TH_HP_01": {
    ...
    "control_parameters": {
        "aggregation_plr_limit": "max"
    },
    "control_modules": [
        {
            "name": "storage_driven",
            "high_threshold": 0.95,
            "low_threshold": 0.3,
            "storage_uac": "TST_TH_BFT_01"
        },
         {
            "name": "storage_driven",
            "high_threshold": 0.99,
            "low_threshold": 0.5,
            "storage_uac": "TST_TH_BFT_02"
        }
    ],
    ...
}
```

#### Economical discharge
Handles the discharging of a battery to only be allowed if sufficient charge is available and a linked PV plant has available power below a given threshold. Mostly used for examplatory purposes.

**Note:** At the moment there is no mechanism to prevent the battery to be fully discharged in a single timestep. This will be changed in a future update.

This module is implemented for the following component types: `Battery`

| | |
| --- | --- |
| **name** | Name of the module. Fixed value of `economical_discharge` |
| **pv_threshold** | Treshold of the PV plant below which discharge is allowed. Absolute value in Wh. |
| **min_charge** | The minimum charge level required for discharge to be allowed. Defaults to `0.2`. |
| **discharge_limit** | The charge level to which the battery is discharged, below which discharge is stopped. Defaults to `0.05` |
| **pv_plant_uac** | The UAC of the PV plant that is linked to the module. |
| **battery_uac** | The UAC of the battery to which the module is attached. |

#### Profile limited
Sets the maximum PLR of a component to values from a profile. Used to set the operation of a component to a fixed schedule while allowing circumstances to override the schedule in favour of a lower PLR.

This module is implemented for the following component types: `CHPP`, `Electrolyser`, `FuelBoiler`, `HeatPump`

| | |
| --- | --- |
| **name** | Name of the module. Fixed value of `profile_limited` |
| **profile_path** | File path to the profile with the limit values. Must be a `.prf` file. |

#### Storage-driven
Controls a component to only operate when the charge of a linked storage component falls below a certain threshold and keep operating until a certain higher threshold is reached and minimum operation time has passed. This is often used to avoid components switching on and off rapidly to keep a storage topped up, as realised systems often operate with this kind of hysteresis behaviour.

This module is implemented for the following component types: `CHPP`, `Electrolyser`, `FuelBoiler`, `HeatPump`

| | |
| --- | --- |
| **name** | Name of the module. Fixed value of `storage_driven` |
| **low_threshold** | The storage charge threshold below which operation is turned on. Defaults to `0.2`.
| **high_treshold** | The storage charge threshold above which operation is turned off. Defaults to `0.95`.
| **min_run_time** | Minimum run time for the "on" state. Absolute value in seconds. Defaults to `1800`.
| **storage_uac** | The UAC of the storage component linked to the module.

#### Temperature sorting
Controls a component so that the availabe energies of the inputs/outputs during calculation of the `potential` and `process` steps are sorted by the temperatures they provide/request. This is useful for components where the temperature differences matter for the calculation. For example a heat pump can use the heat source with the highest temperature first for improved efficiency.

**Note:** This will overwrite the order defined in the bus!

This module is implemented for the following component types: `HeatPump`

| | |
| --- | --- |
| **name** | Name of the module. Fixed value of `temperature_sorting` |
| **input_temps** | Sets if the inputs are sorted by minimum or maximum temperature. Should be `max` (default) or `min`.
| **input_order** | Sets the direction in which the inputs are sorted. Should be `asc` or `desc` (default).
| **output_temps** | Sets if the outputs are sorted by minimum or maximum temperature. Should be `max` or `min` (default).
| **output_order** | Sets the direction in which the outputs are sorted. Should be `asc` (default) or `desc`.

## Boundary and connection components

### General bounded sink
| | |
| --- | --- |
| **Type name** | `BoundedSink`|
| **File** | `energy_systems/general/bounded_sink.jl` |
| **System function** | `bounded_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | |
| **Tracked values** | `IN`, `Max_Energy`, `Temperature` |

Generalised implementation of a bounded sink.

Can be given a profile for the maximum power it can take in, which is scaled by the given scale factor. If the medium supports it, a temperature can be given, either as profile from a .prf file or from the ambient temperature of the project-wide weather file or a constant temperature can be set.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `max_power_profile_file_path` | `String` | N/N | `profiles/district/max_power.prf` | Path to the max power profile. |
| `constant_power` | `Temperature` | N/N | 4000.0 | If given, sets the max power of the input to a constant value. |
| `scale` | `Float` | N/Y | 1.0 | Factor by which the max power values are multiplied. Only applies to profiles. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the input temperature. |
| `constant_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the input to a constant value. |
| `temperature_from_global_file` | `String` | N/N | ` temp_ambient_air` | If given, sets the temperature of the input to the ambient air temperature of the global weather file. |

Note that either `temperature_profile_file_path`, `constant_temperature` **or** `temperature_from_global_file` (or none of them) should be given!

### General bounded supply
| | |
| --- | --- |
| **Type name** | `BoundedSupply`|
| **File** | `energy_systems/general/bounded_supply.jl` |
| **System function** | `bounded_source` |
| **Medium** | `medium`/`None` |
| **Input media** | |
| **Output media** | `None`/`auto` |
| **Tracked values** | `OUT`, `Max_Energy`, `Temperature` |

Generalised implementation of a bounded source.

Can be given a profile for the maximum power it can provide, which is scaled by the given scale factor. If the medium supports it, a temperature can be given, either as profile from a .prf file or from the ambient temperature of the project-wide weather file or a constant temperature can be set.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `max_power_profile_file_path` | `String` | N/N | `profiles/district/max_power.prf` | Path to the max power profile. |
| `constant_power` | `Temperature` | N/N | 4000.0 | If given, sets the max power of the output to a constant value. |
| `scale` | `Float` | N/Y | 1.0 | Factor by which the max power values are multiplied. Only applies to profiles. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the output temperature. |
| `constant_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the output to a constant value. |
| `temperature_from_global_file` | `String` | N/N | ` temp_ambient_air` | If given, sets the temperature of the input to the ambient air temperature of the global weather file. |

Note that either `temperature_profile_file_path`, `constant_temperature` **or** `temperature_from_global_file` (or none of them) should be given!

### Bus
| | |
| --- | --- |
| **Type name** | `Bus`|
| **File** | `energy_systems/connections/bus.jl` |
| **System function** | `bus` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |
| **Tracked values** | `Balance`, `Transfer->UAC` |

The only implementation of special component `Bus`, used to connect multiple components with a shared medium.

Note that the tracked value `Transfer->UAC` refers to an output value that corresponds to how much energy the bus has transfered to the bus with the given UAC.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `connections` | `Dict{String,Any}` | N/N |  | Connection config for the bus. See [chapter on the input file format](resie_input_file_format.md) for details. |

### General fixed sink
| | |
| --- | --- |
| **Type name** | `FixedSink`|
| **File** | `energy_systems/general/fixed_sink.jl` |
| **System function** | `fixed_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | |
| **Tracked values** | `IN`, `Demand`, `Temperature` |

Generalised implementation of a fixed sink.

Can be given a profile for the energy it requests, which is scaled by the given scale factor. Alternatively a static load can be given. If the medium supports it, a temperature can be given, either as profile from a .prf file or from the ambient temperature of the project-wide weather file or a constant temperature can be set.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `energy_profile_file_path` | `String` | N/N | `profiles/district/demand.prf` | Path to the input energy profile. |
| `constant_demand` | `Float` | N/N | 4000.0 | [power, not work!] If given, ignores the energy profile and sets the input demand to this constant power. |
| `scale` | `Float` | N/Y | 1.0 | Factor by which the energy profile values are multiplied. Only applies to profiles. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the input temperature. |
| `constant_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the input to a constant value. |
| `temperature_from_global_file` | `String` | N/N | ` temp_ambient_air` | If given, sets the temperature of the input to the ambient air temperature of the global weather file. |

Note that either `temperature_profile_file_path`, `constant_temperature` **or** `temperature_from_global_file` (or none of them) should be given!

### General demand
| | |
| --- | --- |
| **Type name** | `Demand`|
| **File** | `energy_systems/general/fixed_sink.jl` |
Alias to `FixedSink`.

### General fixed supply
| | |
| --- | --- |
| **Type name** | `FixedSupply`|
| **File** | `energy_systems/general/fixed_supply.jl` |
| **System function** | `fixed_source` |
| **Medium** | `medium`/`None` |
| **Input media** |  |
| **Output media** | `None`/`auto` |
| **Tracked values** | `OUT`, `Supply`, `Temperature` |

Generalised implementation of a fixed source.

Can be given a profile for the energy it can provide, which is scaled by the given scale factor. If the medium supports it, a temperature can be given, either as profile from a .prf file or from the ambient temperature of the project-wide weather file or a constant temperature can be set.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `energy_profile_file_path` | `String` | N/N | `profiles/district/energy_source.prf` | Path to the output energy profile. |
| `constant_supply` | `Float` | N/N | 4000.0 | [power, not work!] If given, ignores the energy profile and sets the output supply to this constant power. |
| `scale` | `Float` | N/Y | 1.0 | Factor by which the energy profile values are multiplied. Only applies to profiles. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the output temperature. |
| `constant_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the output to a constant value. |
| `temperature_from_global_file` | `String` | N/N | ` temp_ambient_air` | If given, sets the temperature of the input to the ambient air temperature of the global weather file. |

Note that either `temperature_profile_file_path`, `constant_temperature` **or** `temperature_from_global_file` (or none of them) should be given!

### Grid connection
| | |
| --- | --- |
| **Type name** | `GridConnection`|
| **File** | `energy_systems/connections/grid_connection.jl` |
| **System function** | `bounded_source`, `bounded_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |
| **Tracked values** | `IN`, `OUT`, `Input_sum`, `Output_sum`, `Temperature` |

Used as a source or sink with no limit, which receives or gives off energy from/to outside the system boundary. Optionally, temperatures can be taken into account (constant, from profile or from weather file).

If parameter `is_source` is true, acts as a `bounded_source` with only one output connection. Otherwise a `bounded_sink` with only one input connection. In both cases the amount of energy supplied/taken in is tracked as a cumulutative value.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `is_source` | `Boolean` | Y/Y | `True` | If true, the grid connection acts as a source. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the input temperature. |
| `constant_temperature` | `Temperature` | N/N | 12.0 | If given, sets the temperature of the input (or output) to a constant value. |
| `temperature_from_global_file` | `String` | N/N | `temp_ambient_air` | If given, sets the temperature of the input (or output) to the ambient air temperature of the global weather file. |

Note that either `temperature_profile_file_path`, `constant_temperature` **or** `temperature_from_global_file` (or none of them) should be given!

## Other sources and sinks

### Photovoltaic plant
| | |
| --- | --- |
| **Type name** | `PVPlant`|
| **File** | `energy_systems/electric_producers/pv_plant.jl` |
| **System function** | `fixed_source` |
| **Medium** | |
| **Input media** | |
| **Output media** | `m_el_out`/`m_e_ac_230v` |
| **Tracked values** | `OUT`, `Supply` |

A photovoltaic (PV) power plant producing electricity.

The energy it produces in each time step must be given as a profile, but can be scaled by a fixed value.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `energy_profile_file_path` | `String` | Y/N | `profiles/district/pv_output.prf` | Path to the output energy profile. |
| `scale` | `Float` | Y/N | 4000.0 | Factor by which the profile values are multiplied. |

## Transformers

### Combined Heat and Power plant
| | |
| --- | --- |
| **Type name** | `CHPP`|
| **File** | `energy_systems/electric_producers/chpp.jl` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_gas_in`/`m_c_g_natgas` |
| **Output media** | `m_heat_out`/`m_h_w_ht1`, `m_el_out`/`m_e_ac_230v` |
| **Tracked values** | `IN`, `OUT`, `Losses` |

A Combined Heat and Power Plant (CHPP) that transforms fuel into heat and electricity.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `power_el` | `Float` | Y/N | 4000.0 | The design power of electrical output. |
| `min_power_fraction` | `Float` | Y/Y | 0.2 | The minimum fraction of the design power that is required for the plant to run. |
| `min_run_time` | `UInt` | Y/Y | 1800 | Minimum run time of the plant in seconds. Will be ignored if other constraints apply. |
| `output_temperature` | `Temperature` | N/N | 90.0 | The temperature of the heat output. |
| `efficiency_fuel_in` | `String` | Y/Y | `const:1.0` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_el_out` | `String` | Y/Y | `pwlin:0.01,0.17,0.25,0.31,0.35,0.37,0.38,0.38,0.38` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_heat_out` | `String` | Y/Y | `pwlin:0.8,0.69,0.63,0.58,0.55,0.52,0.5,0.49,0.49` | See [description of efficiency functions](#efficiency-functions). |
| `linear_interface` | `String` | Y/Y | `fuel_in` | See [description of efficiency functions](#efficiency-functions). |
| `nr_discretization_steps` | `UInt` | Y/Y | `8` | See [description of efficiency functions](#efficiency-functions). |

### Electrolyser
| | |
| --- | --- |
| **Type name** | `Electrolyser`|
| **File** | `energy_systems/others/electrolyser.jl` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_el_in`/`m_e_ac_230v` |
| **Output media** | `m_heat_ht_out`/`m_h_w_ht1`, `m_heat_lt_out`/`m_h_w_lt1`, `m_h2_out`/`m_c_g_h2`, `m_o2_out`/`m_c_g_o2` |
| **Tracked values** | `IN`, `OUT`, `Losses`, `Losses_heat`, `Losses_hydrogen` |

Implementation of an electrolyser splitting pute water into hydrogen and oxygen while providing the waste heat as output.

If parameter `heat_lt_is_usable` is false, the output interface `m_heat_lt_out` is not set and does not require to be connected to another component or bus. The energy that is calculated to be put out on this interface is then added to `Losses_heat` instead.

**Dispatch strategies:**

* `all_equal`: This spreads the load evenly across all units. This is a simplified model that ignores `min_power_fraction`.
* `equal_with_mpf`: Same as an equal distribution, however if the total PLR is lower than `min_power_fraction`, then a number of units are activated at a calculated PLR to ensure the minimum restriction is observed and the demand is met.
* `try_optimal`: Attempts to activate a number of units close to their optimal PLR to meet the demand. If no optimal solution exists, typically at very low PLR or close to the nominal power, falls back to activating only one or all units.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `power_el` | `Float` | Y/N | 4000.0 | The maximum electrical design power input. |
| `nr_switchable_units` | `UInt` | Y/Y | 1 | The number of units that can be switched on/off to meet demand. |
| `dispatch_strategy` | `String` | Y/Y | `equal_with_mpf` | The dispatch strategy to be used to switch on/off units. |
| `min_power_fraction` | `Float` | Y/Y | 0.4 | The minimum PLR that is required for one unit of the electrolyser to run. |
| `min_power_fraction_total` | `Float` | Y/Y | 0.2 | The minimum PLR that is required for the whole plant to run. |
| `optimal_unit_plr` | `Float` | Y/Y | 0.65 | The optimal PLR for each unit at which hydrogen production is most efficient. Only required if dispatch strategy `try_optimal` is used. |
| `min_run_time` | `UInt` | Y/Y | 3600 | Minimum run time of the plant in seconds. Will be ignored if other constraints apply. |
| `heat_lt_is_usable` | `Bool` | Y/Y | false | Toggle if the low temperature heat output is usable. |
| `output_temperature_ht` | `Temperature` | Y/Y | 55.0 | The temperature of the high temperature heat output. |
| `output_temperature_lt` | `Temperature` | Y/Y | 25.0 | The temperature of the low temperature heat output. |
| `linear_interface` | `String` | Y/Y | `el_in` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_el_in` | `String` | Y/Y | `const:1.0` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_heat_ht_out` | `String` | Y/Y | `const:0.15` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_heat_lt_out` | `String` | Y/Y | `const:0.07` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_h2_out` | `String` | Y/Y | `const:0.57` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_h2_out_lossless` | `String` | Y/Y | `const:0.6` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_o2_out` | `String` | Y/Y | `const:0.6` | See [description of efficiency functions](#efficiency-functions). |
| `nr_discretization_steps` | `UInt` | Y/Y | `1` | See [description of efficiency functions](#efficiency-functions). |

### Fuel boiler
| | |
| --- | --- |
| **Type name** | `FuelBoiler`|
| **File** | `energy_systems/heat_producers/fuel_boiler.jl` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_fuel_in` |
| **Output media** | `m_heat_out`/`m_h_w_ht1` |
| **Tracked values** | `IN`, `OUT`, `Losses` |

A boiler that transforms chemical fuel into heat.

This needs to be parameterized with the medium of the fuel intake as the implementation is agnostic towards the kind of fuel under the assumption that the fuel does not influence the behaviour or require/produce by-products such as pure oxygen or ash (more to the point, the by-products do not need to be modelled for an energy simulation.)

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `m_fuel_in` | `String` | Y/N | `m_c_g_natgas` | The medium of the fuel intake. |
| `power_th` | `Float` | Y/N | 4000.0 | The maximum thermal design power output. |
| `min_power_fraction` | `Float` | Y/Y | 0.1 | The minimum fraction of the design power_th that is required for the plant to run. |
| `min_run_time` | `UInt` | Y/Y | 0 | Minimum run time of the plant in seconds. Will be ignored if other constraints apply. |
| `output_temperature` | `Temperature` | N/N | 90.0 | The temperature of the heat output. |
| `efficiency_fuel_in` | `String` | Y/Y | `const:1.1` | See [description of efficiency functions](#efficiency-functions). |
| `efficiency_heat_out` | `String` | Y/Y | `const:1.0` | See [description of efficiency functions](#efficiency-functions). |
| `linear_interface` | `String` | Y/Y | `heat_out` | See [description of efficiency functions](#efficiency-functions). |
| `nr_discretization_steps` | `UInt` | Y/Y | `30` | See [description of efficiency functions](#efficiency-functions). |

### Heat pump
| | |
| --- | --- |
| **Type name** | `HeatPump`|
| **File** | `energy_systems/heat_producers/heat_pump.jl` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_el_in`/`m_e_ac_230v`, `m_heat_in`/`m_h_w_lt1` |
| **Output media** | `m_heat_out`/`m_h_w_ht1` |
| **Tracked values** | `IN`, `OUT`, `COP`, `MixingTemperature_Input`, `MixingTemperature_Output` |

Elevates supplied low temperature heat to a higher temperature with input electricity.

| Name | Type | R/D | Example | Unit | Description |
| ----------- | ------- | --- | --- | ------------------------ | ------------------------ |
| `power_th` | `Float` | Y/N | 4000.0 | [W] | The thermal design power at the heating output. This must be maximal value considering the max power function, as that is normalised to 1.0. |
| `cop_function` | `String` | Y/Y | `carnot:0.4:const:1.0` | [-] |  See [description of function definitions](#cop-functions). The function for the the dynamic COP with the temperature-dependent part in the first function and the PLR-dependent part in the second.
| `bypass_cop` | `Float` | Y/Y | 15.0 | [-] |  A constant COP value used for bypass operation. |
| `max_power_function` | `String` | Y/Y | `const:1.0` | [-] |  See [description of function definitions](#power-functions). The function for the maximum power as fraction of nominal power. |
| `min_power_function` | `String` | Y/Y | `const:0.2` | [-] |  See [description of function definitions](#power-functions). The function for the minimum power as fraction of nominal power. |
| `consider_icing` | `Bool` | N/Y | false | [-] |  If true, enables the calculation of icing losses. |
| `icing_coefficients` | `String` | N/Y | `3,-0.42,15,2,30` | [-] |  Parameters for the icing losses model. For details, see [this section](resie_energy_system_components.md#icing-losses-of-heat-pumps-with-air-as-source-medium)|
| `input_temperature` | `Temperature` | N/N | 20.0 | [°C] |  If given, the supplied temperatures at the heat pump input are ignored and the provided constant one is used. |
| `output_temperature` | `Temperature` | N/N | 65.0 | [°C] |  If given, the output temperatures at the heat pump output are ignored and the provided constant one is used. |
| `optimise_slice_dispatch` | `Bool` | N/Y | false | [-] |  If true, enables the optimisation of slice dispatch. |
| `optimal_plr` | `Float` | N/N | 0.45 | [-] |  The PLR at which efficiency is highest. Only used for slice dispatch optimisation. |
| `nr_optimisation_passes` | `UInt` | N/Y | 10 | [-] |  The number of passes the optimisation algorithm performs if optimise_slice_dispatch is true. Note that this heavily impacts performance. |

#### Exemplary input file definition for HeatPump
**Simple heat pump with constant COP and fixed output temperature**
```json
"TST_TH_HP_01": {
    "type": "HeatPump",
    "output_refs": ["TST_TH_BUS_01"],
    "power_th": 12000,
    "cop_function": "const:3.0",
    "output_temperature": 70.0
}
```

**Air-sourced heat pump with dynamic COP and variable power from data sheets**
```json
"TST_TH_HP_01": {
    "type": "HeatPump",
    "output_refs": ["TST_TH_BUS_01"],
    "power_th": 20000,
    "cop_function": "field:0,45,55,65,75,85,95,105;0,3.79,3.26,2.87,2.57,2.34,2.15,1.99;10,4.59,3.79,3.26,2.87,2.57,2.34,2.15;20,5.93,4.59,3.79,3.26,2.87,2.57,2.34;30,8.74,5.93,4.59,3.79,3.26,2.87,2.57;40,20.15,8.74,5.93,4.59,3.79,3.26,2.87;50,20.15,20.15,8.74,5.93,4.59,3.79,3.26;60,20.15,20.15,20.15,8.74,5.93,4.59,3.79;70,20.15,20.15,20.15,20.15,8.74,5.93,4.59;80,20.15,20.15,20.15,20.15,20.15,8.74,5.93;90,20.15,20.15,20.15,20.15,20.15,20.15,8.74;100,20.15,20.15,20.15,20.15,20.15,20.15,20.15:poly:0.4,0.6",
    "max_power_function": "poly-2:0.6625,0.0008929,-0.001",
    "min_power_function": "poly-2:0.5125,0.0001786,-0.001",
    "bypass_cop": 20.15,
    "consider_icing": true
}
```


## Storage

### General storage
| | |
| --- | --- |
| **Type name** | `Storage`|
| **File** | `energy_systems/general/storage.jl` |
| **System function** | `storage` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |
| **Tracked values** | `IN`, `OUT`, `Load`, `Load%`, `Capacity`, `Losses` |

A generic implementation for energy storage technologies.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `capacity` | `Float` | Y/N | 12000.0 | The overall capacity of the storage. |
| `load` | `Float` | Y/N | 6000.0 | The initial load state of the storage. |

### Battery
| | |
| --- | --- |
| **Type name** | `Battery`|
| **File** | `energy_systems/storage/battery.jl` |
| **System function** | `storage` |
| **Medium** | `medium`/`m_e_ac_230v` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |
| **Tracked values** | `IN`, `OUT`, `Load`, `Load%`, `Capacity`, `Losses` |

A storage for electricity.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `capacity` | `Float` | Y/N | 12000.0 | The overall capacity of the battery. |
| `load` | `Float` | Y/N | 6000.0 | The initial load state of the battery. |

### Buffer Tank
| | |
| --- | --- |
| **Type name** | `BufferTank`|
| **File** | `energy_systems/storage/buffer_tank.jl` |
| **System function** | `storage` |
| **Medium** | `medium`/`m_h_w_ht1` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |
| **Tracked values** | `IN`, `OUT`, `Load`, `Load%`, `Capacity`, `Losses` |

A short-term storage for heat of thermal carrier fluids, typically water.

If the adaptive temperature calculation is activated, the temperatures for the input/output of the BT depends on the load state. If it is sufficiently full (depends on the `switch_point`), the BT can output at the `high_temperature` and takes in at the `high_temperature`. If the load falls below that, the output temperature drops and reaches the `low_temperature` as the load approaches zero.

If the adaptive temperature calculation is deactivated, always assumes the `high_temperature` for both input and output.


| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `capacity` | `Float` | Y/N | 12000.0 | The overall capacity of the BT. |
| `load` | `Float` | Y/N | 6000.0 | The initial load state of the BT. |
| `use_adaptive_temperature` | `Float` | Y/Y | `False` | If true, enables the adaptive output temperature calculation. |
| `switch_point` | `Float` | Y/Y | 0.15 | Partial load at which the adaptive output temperature calculation switches. |
| `high_temperature` | `Temperature` | Y/Y | 75.0 | The high end of the adaptive in-/output temperature. |
| `low_temperature` | `Temperature` | Y/Y | 20.0 | The low end of the adaptive in-/output temperature. |

### Seasonal thermal storage
| | |
| --- | --- |
| **Type name** | `SeasonalThermalStorage`|
| **File** | `energy_systems/storage/seasonal_thermal_storage.jl` |
| **System function** | `storage` |
| **Medium** |  |
| **Input media** | `m_heat_in`/`m_h_w_ht1` |
| **Output media** | `m_heat_out`/`m_h_w_lt1` |
| **Tracked values** | `IN`, `OUT`, `Load`, `Load%`, `Capacity`, `Losses` |

A long-term storage for heat stored in a stratified artificial aquifer.

If the adaptive temperature calculation is activated, the temperatures for the input/output of the STES depends on the load state. If it is sufficiently full (depends on the `switch_point`), the STES can output at the `high_temperature` and takes in at the `high_temperature`. If the load falls below that, the output temperature drops and reaches the `low_temperature` as the load approaches zero.

If the adaptive temperature calculation is deactivated, always assumes the `high_temperature` for both input and output.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `capacity` | `Float` | Y/N | 12000.0 | The overall capacity of the STES. |
| `load` | `Float` | Y/N | 6000.0 | The initial load state of the STES. |
| `use_adaptive_temperature` | `Float` | Y/Y | `False` | If true, enables the adaptive output temperature calculation. |
| `switch_point` | `Float` | Y/Y | 0.25 | Partial load at which the adaptive output temperature calculation switches. |
| `high_temperature` | `Temperature` | Y/Y | 90.0 | The high end of the adaptive in-/output temperature. |
| `low_temperature` | `Temperature` | Y/Y | 15.0 | The low end of the adaptive in-/output temperature. |


## Heat sources and sinks

### Generic heat source
| | |
| --- | --- |
| **Type name** | `GenericHeatSource`|
| **File** | `energy_systems/heat_sources/generic_heat_source.jl` |
| **System function** | `bounded_source` |
| **Medium** | `medium`/`None` |
| **Input media** | |
| **Output media** | `None`/`auto` |
| **Tracked values** | `OUT`, `Max_Energy`, `Temperature_src_in`, `Temperature_snk_out` |

A generic heat source for various sources of heat.

Can be given a profile for the maximum power it can provide, which is scaled by the given scale factor. For the temperature either `temperature_profile_file_path`, `constant_temperature` **or** `temperature_from_global_file` **must** be given! The given temperature is considered the input source temperature and an optional reduction is applied (compare with [model description](resie_energy_system_components.md#generic-heat-source)). If the `lmtd` model is used and no min/max temperatures are given, tries to read them from the given profile.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `max_power_profile_file_path` | `String` | N/N | `profiles/district/max_power.prf` | Path to the max power profile. |
| `constant_power` | `Temperature` | N/N | 4000.0 | If given, sets the max power of the input to a constant value. |
| `scale` | `Float` | N/Y | 1.0 | Factor by which the max power values are multiplied. Only applies to profiles. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the input temperature. |
| `constant_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the input to a constant value. |
| `temperature_from_global_file` | `String` | N/N | `temp_ambient_air` | If given, sets the temperature of the input to the ambient air temperature of the global weather file. |
| `temperature_reduction_model` | `String` | Y/Y | `none` | Which temperature reduction model is used. Should be one of: `none`, `constant`, `lmtd` |
| `min_source_in_temperature` | `Float` | N/N | -10.0 | Minimum source input temperature. |
| `max_source_in_temperature` | `Float` | N/N | 40.0 | Maximum source input temperature. |
| `minimal_reduction` | `Float` | N/Y | 2.0 | Minimal reduction temperature. For the `constant` model this exact value is used, for `lmtd` a slight correction is applied. |

**Exemplary input file definition for GenericHeatSource**

```JSON
"TST_SRC_01": {
    "type": "GenericHeatSource",
    "medium": "m_h_w_lt1",
    "control_refs": [],
    "output_refs": [
        "TST_BUS_TH_01"
    ],
    "max_power_profile_file_path": "./profiles/tests/source_heat_max_power.prf",
    "temperature_profile_file_path": "./profiles/examples/general/src_heat_temp_var_avg25.prf",
    "temperature_reduction_model": "lmtd",
    "min_source_in_temperature": 5,
    "max_source_in_temperature": 35,
    "scale": 2000
}
```


### Geothermal probes
| | |
| --- | --- |
| **Type name** | `GeothermalProbes`|
| **File** | `energy_systems/heat_sources/geothermal_probes.jl` |
| **System function** | `storage` |
| **Medium** |  |
| **Input media** | `m_heat_in`/`m_h_w_ht1` |
| **Output media** | `m_heat_out`/`m_h_w_lt1` |
| **Tracked values** | `IN`, `OUT`, `new_fluid_temperature`, `current_output_temperature`, `fluid_reynolds_number` |

A model of a geothermal probe field or a single geothermal probe. Two models are available, one `detailed` and a `simplified` version that uses a constant user-defined thermal borehole resistance. This avoids the need of defining 11 additional parameters.

**Model `simplified`:**

The geothermal probe is modeled using precalculated g-functions. The model needs quite many input parameters. Especially the soil properties, including the undisturbed ground temperature, have a significant effect on the results. Therefore is it crucial to know the soil conditions at the investigated site. 

The g-function is taken from the library provided within the repository. There are different configurations available: rectangle, open_rectangle, zoned_rectangle, U_configurations, lopsided_U_configuration, C_configuration, L_configuration. Each of them can be specified by the number of probes in x and y direction (note that the number of probes defined for x has to be less or equal the number of probes defined for y). Some of the configurations, like zoned rectangles, require an additional key, that is specified in the documentation of the library in detail, available [here](https://gdr.openei.org/files/1325/LibraryOverview_v11.1%20(1).pdf) within the publication [doi.org/10.15121/1811518](https://doi.org/10.15121/1811518).

A short overview is given in the following. Note that not all configurations are available. Check the documentation linked above or the included text files that contain all possible key combinations for the different probe field configurations.

**rectangle**  
Here, only `number_of_probes_x` and `number_of_probes_y` are required. They define the number of rows in x and y direction, while y >= x. The rectangle that is defined with these two parameters is filled completely with probes.

<pre>
Example:
o o o  
o o o  
o o o  
o o o  
</pre>

number_of_probes_x = 3  
number_of_probes_y = 4  
key_2 = ""  

**open_rectangle**  
Here, `number_of_probes_x` and `number_of_probes_y` define a probe field as for a normal rectangle. This rectangle is not filled, instead `key_2` defines the number of outer rows that should be considered. This allows for the creation of a single-row rectangle, or a rectangle field that has a "hole" in the middle.

<pre>
Example:
o o o o o  
o o o o o  
o o   o o  
o o   o o  
o o   o o  
o o o o o  
o o o o o  
</pre>

number_of_probes_x = 5  
number_of_probes_y = 7  
key_2 = "2"  

**zoned_rectangle**  
Here, `number_of_probes_x` and `number_of_probes_y` define an unfilled rectangle with only one row of probes (like an open rectancle with `key_2 = 1`). For zoned rectangles, `key_2` then defines the shape of the inner assembly of probes forming a rectangle, which can be "1_3" (as "x_y") for an inner set of 1x3 probes, located inside of the outer ring.

<pre>
Example:
o o o o o  
o       o  
o   o   o  
o   o   o  
o   o   o  
o       o  
o o o o o  
</pre>

number_of_probes_x = 5  
number_of_probes_y = 7  
key_2 = "1_3"  

**U_configurations**  
Here, `number_of_probes_x` and `number_of_probes_y` define the number of probes forming a single-row rectangle that is left open at the top end. The `key_2` then defines the number of rows that are forming this U-shape.

<pre>
Example:
o o   o o  
o o   o o  
o o   o o  
o o o o o  
o o o o o  
</pre>

number_of_probes_x = 5  
number_of_probes_y = 5  
key_2 = "2"  

**lopsided_U_configuration**  
Lopsided U is an U-configuration with some probes missing at the top right corner. This is only available as single-row U. The keys `number_of_probes_x` and `number_of_probes_y` define the general shape of the U, while `key_2` then represents the number of removed probes from the top right corner at the right side of the U. 

<pre>
Example:
o         
o         
o       o  
o       o  
o       o  
o o o o o  
</pre>

number_of_probes_x = 5  
number_of_probes_y = 6  
key_2 = "2"  

**C_configuration**  
C-configurations are only available as single-row C-shapes, where the C is turned 90° anti-clockwise. A C-shape is like an U-shape with some more probes at the top row attempting to close the U to form an open rectangle. `number_of_probes_x` and `number_of_probes_y` define the number of probes forming an unfilled single-row rectangle, while `key_2` defines the number of probes that are removed from the top end of the rectangle. If possible, they are removed symmetrically starting from the center. If that is not possible due to an uneven number, the single leftover probe is removed at the left side.

<pre>
Example:
o o     o o  
o         o  
o         o  
o         o  
o         o  
o o o o o o  
</pre>

number_of_probes_x = 6  
number_of_probes_y = 6  
key_2 = "2"  

**L_configuration**  
L-configurations are currently only available as single-row L shapes. They are defined like rectangles, but the probe field then only contains a L with a single row that is not filled with other probes.

<pre>
Example:
o   
o   
o   
o   
o o o  
</pre>

number_of_probes_x = 3  
number_of_probes_y = 5  
key_2 = ""  


| Name | Type | R/D | Example | Unit | Description |
| ----------- | ------- | --- | --- | ------------------------ | ------------------------ |
| `model_type` | `String` | Y/Y | `simplified` | [-] | Type of probe model: "simplified" with constant or "detailed" with calculated thermal borehole resistance in every time step. |
| `probe_field_geometry` | `String` | Y/Y | `rectangle` | [-] | type of probe field geometry, can be one of: rectangle, open_rectangle, zoned_rectangle, U_configurations, lopsided_U_configuration, C_configuration, L_configuration |
| `number_of_probes_x` | `Int` | Y/Y | 1 | [-] | number of probes in x direction, corresponds to value of g-function library. Note that number_of_probes_x <= number_of_probes_y! |
| `number_of_probes_y` | `Int` | Y/Y | 1 | [-] | number of probes in y direction, corresponds to value of g-function library. Note that number_of_probes_x <= number_of_probes_y! |
| `probe_field_key_2` | `String` | Y/Y | "" | [-] | key2 of g-function library. Can also be "" if none is needed. The value depends on the chosen library type. |
| `probe_depth` | `Float` | Y/Y | 150 | [m] | depth (or length) of a single geothermal probe. Has to be between 24 m and 384 m. |
| `borehole_spacing` | `Float` | Y/Y | 5 | [m] | distance between boreholes in the field, assumed to be constant. Set average spacing.  |
| `borehole_diameter` | `Float` | Y/Y | 0.15 | [m] | borehole diameter |
| `borehole_thermal_resistance` | `Float` | Y/Y | 0.1 | [(Km)/W] | thermal resistance of borehole (constant, if not calculated from other parameters in every time step!) |
| `loading_temperature` | `Temperature` | N/Y | nothing | [°C] | nominal high temperature for loading geothermal probe storage, can also be set from other end of interface |
| `loading_temperature_spread` | `Float` | Y/Y | 3 | [K] | temperature spread between forward and return flow during loading |
| `unloading_temperature_spread` | `Float` | Y/Y | 3 | [K] | temperature spread between forward and return flow during unloading |
| `boreholewall_start_temperature` | `Float` | Y/Y | 4 | [°C] | borehole wall starting temperature |
| `soil_undisturbed_ground_temperature` | `Float` | Y/Y | 11 | [°C] | undisturbed ground temperature as average over the depth of the probe, considered as constant over time |
| `soil_heat_conductivity` | `Float` | Y/Y | 1.5 | [W/(Km)] | heat conductivity of surrounding soil, homogenous and constant |
| `soil_density` | `Float` | Y/Y | 2000 | [kg/m^3] | soil density |
| `soil_specific_heat_capacity` | `Float` | Y/Y | 2400 | [J/(kgK)] | soil specific heat capacity |
| `max_input_power` | `Float` | Y/Y | 50 | [W/m_probe] | maximum input power per probe meter |
| `max_output_power` | `Float` | Y/Y | 50 | [W/m_probe] | maximum output power per probe meter |
| `regeneration` | `Bool` | Y/Y | true | [-] | flag if regeneration should be taken into account |

**Model `detailed`:**

The detailed model uses extended parameters to determine the thermal borehole resistance from the fluid to the soil. Therefore, an approach by Hellström (1991) is used to determine the effective thermal borehole resistance using the convective heat transfer coefficient within the pipe. For that, the Reynolds number is calculated in every timestep to determine the heat transmission from fluid to the pipe. The heat conductivity of the pipe and the grout has to be given. The heat transmission from pipe to grout and grout to soil is neglected.

To perform this calculation in every timestep, the following input parameters are required additionally to the ones of the simplified model, while the `borehole_thermal_resistance` is not needed anymore:

| Name | Type | R/D | Example | Unit | Description |
| ----------- | ------- | --- | --- | ------------------------ | ------------------------ |
| `probe_type` | `Int` | Y/Y | 2 | [-] | probe type: 1: single U-pipe in one probe, 2: double U-pipe in one probe |
| `pipe_diameter_outer` | `Float` | Y/Y | 0.032 | [m] | outer pipe diameter |
| `pipe_diameter_inner` | `Float` | Y/Y | 0.026 | [m] | inner pipe diameter |
| `pipe_heat_conductivity` | `Float` | Y/Y | 0.42 | [W/(Km)] | heat conductivity of inner pipes |
| `shank_spacing` | `Float` | Y/Y | 0.1 | [m] | distance between inner pipes in borehole, diagonal through borehole center. required for calculation of thermal borehole resistance. |
| `fluid_specific_heat_capacity` | `Float` | Y/Y | 3800 | [J/(kgK)] | specific heat capacity of brine at 0 °C (25 % glycol 75 % water)  |
| `fluid_density` | `Float` | Y/Y | 1045 | [kg/m^3] | density of brine at 0 °C (25 % glycol 75 % water) |
| `fluid_kinematic_viscosity` | `Float` | Y/Y | 3.9e-6 | [m^2/s] | kinematic viscosity of brine at 0 °C (25 % glycol 75 % water)  |
| `fluid_heat_conductivity` | `Float` | Y/Y | 0.5 | [W/(Km)] | heat conductivity of brine at 0 °C (25 % glycol 75 % water) |
| `fluid_prandtl_number` | `Float` | Y/Y | 30 | [-] | Prandtl-number of brine at 0 °C (25 % glycol 75 % water)  |
| `grout_heat_conductivity` | `Float` | Y/Y | 2.0 | [W/(Km)] | heat conductivity of grout (filling material)  |


**Exemplary input file definition for GeothermalProbe:**

```JSON
"TST_GTP_01": {
    "type": "GeothermalProbes",
    "m_heat_out": "m_h_w_lt1",
    "control_refs": [],
    "output_refs": [
        "TST_HP_01"
    ],
    "model_type": "detailed",
    "___GENERAL PARAMETER___": "",
    "max_output_power": 150,
    "max_input_power": 150,
    "regeneration": true,
    "soil_undisturbed_ground_temperature": 13,
    "soil_heat_conductivity": 1.6 ,
    "soil_density": 1800,
    "soil_specific_heat_capacity": 2400,
    "probe_field_geometry": "rectangle",
    "number_of_probes_x": 3,
    "number_of_probes_y": 12,
    "probe_field_key_2": "",
    "borehole_spacing": 8,
    "probe_depth": 150,
    "borehole_diameter": 0.16,
    "boreholewall_start_temperature": 13,
    "unloading_temperature_spread": 1.5,
    "loading_temperature_spread": 4,
    "___SIMPLIFIED MODEL___": "",
    "borehole_thermal_resistance": 0.1,
    "___DETAILED MODEL___": "",
    "probe_type": 2,
    "pipe_diameter_outer": 0.032,
    "pipe_diameter_inner": 0.0262,
    "pipe_heat_conductivity": 0.42,
    "shank_spacing": 0.1,
    "fluid_specific_heat_capacity": 3795,
    "fluid_density": 1052,
    "fluid_kinematic_viscosity": 3.9e-6,
    "fluid_heat_conductivity": 0.48,
    "fluid_prandtl_number": 31.3,
    "grout_heat_conductivity": 2
}
```