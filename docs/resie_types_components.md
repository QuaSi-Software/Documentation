# Types of energy system components
This document provides details on the component models and their implementations.

The description of each component type includes a block with a number of attributes that describe the type and how it connects to other components by its input and output interfaces. An example of such a block:

| | |
| --- | --- |
| **Type name** | `BoundedSink`|
| **File** | `energy_systems/general/bounded_sink.jl` |
| **Available models** | `default` |
| **System function** | `bounded_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | |

Of particular note are the descriptions of the medium (if it applies) of the component type and its input and output interfaces. The `Medium` is used for components that could handle any type of medium and need to be configured to work with a specific medium. The attributes `Input media` and `Output media` describes which input and output interfaces the type provides and how the media of those can be configured. The syntax `name:value` lists the name of the parameter in the input data that defines the medium first, followed by a forward slash and the default value of the medium second, if any. A value of `None` implies that no default is set and therefore it must be given in the input data. A value of `auto` implies that the value is determined with no required input, usually from the `Medium`.

The description further lists which arguments the implementation takes. Let's take a look at an example:

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `max_power_profile_file_path` | `String` | Y/N | `profiles/district/max_power.prf` | Path to the max power profile. |
| `efficiency` | `Float` | Y/Y | 0.8 | Ratio of output over input energies. |
| `static_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the heat output to a static value. |

The name of the entries should match the keys in the input file, which is carried verbatim as entries to the dictionary argument of the component's constructor. The column `R/D` lists if the argument is required (`R`) and if it has a default value (`D`). If the argument has a default value the example value given in the next column also lists what that default value is. Otherwise the example column shows what a value might look like.

The type refers to the type it is expected to have after being parsed by the JSON library. The type `Temperature` is an internal structure and simply refers to either `Float` or `Nothing`, the null-type in Julia. In general, a temperature of `Nothing` implies that any temperature is accepted and only the amount of energy is revelant. More restrictive number types are automatically cast to their superset, but *not* the other way around, e.g: \(UInt \rightarrow Int \rightarrow Float \rightarrow Temperature\). Dictionaries given in the `{"key":value}` notation in JSON are parsed as `Dict{String,Any}`.

## Boundary and connection components

### General bounded sink
| | |
| --- | --- |
| **Type name** | `BoundedSink`|
| **File** | `energy_systems/general/bounded_sink.jl` |
| **Available models** | `default` |
| **System function** | `bounded_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | |

Generalised implementation of a bounded sink.

Must be given a profile for the maximum power it can take in, which is scaled by the given scale factor. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `max_power_profile_file_path` | `String` | Y/N | `profiles/district/max_power.prf` | Path to the max power profile. |
| `scale` | `Float` | Y/N | 4000.0 | Factor by which the max power values are multiplied. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the input temperature. |
| `static_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the input to a static value. |

### General bounded supply
| | |
| --- | --- |
| **Type name** | `BoundedSupply`|
| **File** | `energy_systems/general/bounded_supply.jl` |
| **Available models** | `default` |
| **System function** | `bounded_source` |
| **Medium** | `medium`/`None` |
| **Input media** | |
| **Output media** | `None`/`auto` |

Generalised implementation of a bounded source.

Must be given a profile for the maximum power it can provide, which is scaled by the given scale factor. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `max_power_profile_file_path` | `String` | Y/N | `profiles/district/max_power.prf` | Path to the max power profile. |
| `scale` | `Float` | Y/N | 4000.0 | Factor by which the max power values are multiplied. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the output temperature. |
| `static_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the output to a static value. |

### Bus
| | |
| --- | --- |
| **Type name** | `Bus`|
| **File** | `energy_systems/connections/bus.jl` |
| **Available models** | `default` |
| **System function** | `bus` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |

The only implementation of special component `Bus`, used to connect multiple components with a shared medium.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `connection_matrix` | `Dict{String,Any}` | N/N |  |  |

### General demand
| | |
| --- | --- |
| **Type name** | `Demand`|
| **File** | `energy_systems/general/demand.jl` |
| **Available models** | `default` |
| **System function** | `fixed_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | |

Generalised implementation of a demand.

Must be given a profile for the energy it requests, which is scaled by the given scale factor. Alternatively a static load can be given. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `energy_profile_file_path` | `String` | Y/N | `profiles/district/demand.prf` | Path to the input energy profile. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the input temperature. |
| `scale` | `Float` | Y/N | 4000.0 | Factor by which the energy profile values are multiplied. |
| `static_load` | `Float` | N/N | 4000.0 | If given, ignores the energy profile and sets the input energy to a static value. |
| `static_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the input to a static value. |

### General fixed supply
| | |
| --- | --- |
| **Type name** | `FixedSupply`|
| **File** | `energy_systems/general/fixed_supply.jl` |
| **Available models** | `default` |
| **System function** | `fixed_source` |
| **Medium** | `medium`/`None` |
| **Input media** |  |
| **Output media** | `None`/`auto` |

Generalised implementation of a fixed source.

Must be given a profile for the energy it can provide, which is scaled by the given scale factor. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `energy_profile_file_path` | `String` | Y/N | `profiles/district/energy_source.prf` | Path to the output energy profile. |
| `scale` | `Float` | Y/N | 4000.0 | Factor by which the energy profile values are multiplied. |
| `temperature_profile_file_path` | `String` | N/N | `profiles/district/temperature.prf` | Path to the profile for the output temperature. |
| `static_temperature` | `Temperature` | N/N | 65.0 | If given, sets the temperature of the output to a static value. |

### Grid connection
| | |
| --- | --- |
| **Type name** | `GridConnection`|
| **File** | `energy_systems/connections/grid_connection.jl` |
| **Available models** | `default` |
| **System function** | `bounded_source`, `bounded_sink` |
| **Medium** | `medium`/`None` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |

Used as a source or sink with no limit, which receives or gives off energy from/to outside the system boundary.

If parameter `is_source` is true, acts as a `bounded_source` with only one output connection. Otherwise a `bounded_sink` with only one input connection. In both cases the amount of energy supplied/taken in is tracked as a cumulutative value.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `is_source` | `Boolean` | Y/Y | `True` | If true, the grid connection acts as a source. |

## Other sources and sinks

### Photovoltaic plant
| | |
| --- | --- |
| **Type name** | `PVPlant`|
| **File** | `energy_systems/electric_producers/pv_plant.jl` |
| **Available models** | default: `simplified` |
| **System function** | `fixed_source` |
| **Medium** | |
| **Input media** | |
| **Output media** | `m_el_out`/`m_e_ac_230v` |

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
| **Available models** | default: `simplified` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_gas_in`/`m_c_g_natgas` |
| **Output media** | `m_heat_out`/`m_h_w_ht1`, `m_el_out`/`m_e_ac_230v` |

A Combined Heat and Power Plant (CHPP) that transforms combustible gas into heat and electricity.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `power` | `Float` | Y/N | 4000.0 | The maximum design power. |
| `electricity_fraction` | `Float` | Y/Y | 0.4 | Fraction of the input chemical energy that is output as electricity. |
| `min_power_fraction` | `Float` | Y/Y | 0.2 | The minimum fraction of the design power that is required for the plant to run. |
| `min_run_time` | `UInt` | Y/Y | 1800 | Minimum run time of the plant in seconds. Will be ignored if other constraints apply. |
| `output_temperature` | `Temperature` | N/N | 90.0 | The temperature of the heat output. |

### Electrolyser
| | |
| --- | --- |
| **Type name** | `Electrolyser`|
| **File** | `energy_systems/others/electrolyser.jl` |
| **Available models** | default: `simplified` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_el_in`/`m_e_ac_230v` |
| **Output media** | `m_heat_out`/`m_h_w_lt1`, `m_h2_out`/`m_c_g_h2`, `m_o2_out`/`m_c_g_o2` |

Implementation of an electrolyser splitting water into hydrogen and oxygen while providing the waste heat as output.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `power` | `Float` | Y/N | 4000.0 | The maximum design power. |
| `min_power_fraction` | `Float` | Y/Y | 0.2 | The minimum fraction of the design power that is required for the plant to run. |
| `heat_fraction` | `Float` | Y/Y | 0.4 | Fraction of the input electric energy that is output as heat. |
| `min_run_time` | `UInt` | Y/Y | 1800 | Minimum run time of the plant in seconds. Will be ignored if other constraints apply. |
| `output_temperature` | `Temperature` | N/Y | 55.0 | The temperature of the heat output. |

### Gas boiler
| | |
| --- | --- |
| **Type name** | `GasBoiler`|
| **File** | `energy_systems/heat_producers/gas_boiler.jl` |
| **Available models** | default: `simplified` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_gas_in`/`m_c_g_natgas` |
| **Output media** | `m_heat_out`/`m_h_w_ht1` |

A gas boiler that transforms combustible gas into heat.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `power` | `Float` | Y/N | 4000.0 | The maximum design power. |
| `min_power_fraction` | `Float` | Y/Y | 0.2 | The minimum fraction of the design power that is required for the plant to run. |
| `min_run_time` | `UInt` | Y/Y | 1800 | Minimum run time of the plant in seconds. Will be ignored if other constraints apply. |
| `output_temperature` | `Temperature` | N/N | 90.0 | The temperature of the heat output. |

### Heat pump
| | |
| --- | --- |
| **Type name** | `HeatPump`|
| **File** | `energy_systems/heat_producers/heat_pump.jl` |
| **Available models** | default: `carnot` |
| **System function** | `transformer` |
| **Medium** | |
| **Input media** | `m_el_in`/`m_e_ac_230v`, `m_heat_in`/`m_h_w_lt1` |
| **Output media** | `m_heat_out`/`m_h_w_ht1` |

Elevates supplied low temperature heat to a higher temperature with input electricity.

| Name | Type | R/D | Example | Description |
| ----------- | ------- | --- | ------------------------ | ------------------------ |
| `power` | `Float` | Y/N | 4000.0 | The maximum design power. |
| `min_power_fraction` | `Float` | Y/Y | 0.2 | The minimum fraction of the design power that is required for the plant to run. |
| `min_run_time` | `UInt` | Y/Y | 1800 | Minimum run time of the plant in seconds. Will be ignored if other constraints apply. |
| `fixed_cop` | `Float` | N/N | 3.0 | If given, ignores the dynamic COP calculation and uses a static one. |
| `input_temperature` | `Temperature` | N/N | 20.0 | If given, ignores the supplied temperature and uses a static one. |
| `output_temperature` | `Temperature` | N/N | 65.0 | If given, ignores the requested temperature and uses a static one. |

## Storage

### Battery
| | |
| --- | --- |
| **Type name** | `Battery`|
| **File** | `energy_systems/storage/battery.jl` |
| **Available models** | default: `simplified` |
| **System function** | `storage` |
| **Medium** | `medium`/`m_e_ac_230v` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |

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
| **Available models** | default: `simplified` |
| **System function** | `storage` |
| **Medium** | `medium`/`m_h_w_ht1` |
| **Input media** | `None`/`auto` |
| **Output media** | `None`/`auto` |

A short-term storage for heat of thermal carrier fluids, typically water.

**Model `simplified`:**

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
| **Available models** | default: `simplified` |
| **System function** | `storage` |
| **Medium** |  |
| **Input media** | `m_heat_in`/`m_h_w_ht1` |
| **Output media** | `m_heat_out`/`m_h_w_lt1` |

A long-term storage for heat stored in a stratified artificial aquifer.

**Model `simplified`:**

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
