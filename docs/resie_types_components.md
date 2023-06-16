# Types of energy system components

## Boundary and connection components

### Type: `BoundedSink`
| | |
| --- | --- |
| **File** | `energy_systems/general/bounded_sink.jl` |
| **Available models** | `default` |
| **System function** | `bounded_sink` |
| **Medium** | `custom` |
| **Input media** | `custom` |
| **Output media** | `None` |
| | |

Generalised implementation of a bounded sink.

Must be given a profile for the maximum power it can take in, which is scaled by the given scale factor. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `max_power_profile_file_path` | `String` | N | `profiles/district/max_power.prf` |
| `temperature_profile_file_path` | `String` | N | `profiles/district/temperature.prf` |
| `static_temperature` | `Temperature` | Y | `Nothing` |

### Type: `BoundedSupply`
| | |
| --- | --- |
| **File** | `energy_systems/general/bounded_supply.jl` |
| **Available models** | `default` |
| **System function** | `bounded_source` |
| **Medium** | `custom` |
| **Input media** | `None` |
| **Output media** | `custom` |
| | |

Generalised implementation of a bounded source.

Must be given a profile for the maximum power it can provide, which is scaled by the given scale factor. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `max_power_profile_file_path` | `String` | N | `profiles/district/max_power.prf` |
| `temperature_profile_file_path` | `String` | N | `profiles/district/temperature.prf` |
| `static_temperature` | `Temperature` | Y | `Nothing` |

### Type: `Bus`
| | |
| --- | --- |
| **File** | `energy_systems/connections/bus.jl` |
| **Available models** | `default` |
| **System function** | `bus` |
| **Medium** | `custom` |
| **Input media** | `any` |
| **Output media** | `any` |
| | |

The only implementation of special component `Bus`, used to connect multiple components with a shared medium.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `medium` | `String` | N | `m_e_ac_230v` |

### Type: `Demand`
| | |
| --- | --- |
| **File** | `energy_systems/general/demand.jl` |
| **Available models** | `default` |
| **System function** | `fixed_sink` |
| **Medium** | `custom` |
| **Input media** | `custom` |
| **Output media** | `None` |
| | |

Generalised implementation of a demand.

Must be given a profile for the energy it requests, which is scaled by the given scale factor. Alternatively a static load can be given. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `energy_profile_file_path` | `String` | N | `profiles/district/demand.prf` |
| `temperature_profile_file_path` | `String` | N | `profiles/district/temperature.prf` |
| `scale` | `Float` | N | 4000 |
| `static_load` | `Float` | Y | `Nothing` |
| `static_temperature` | `Temperature` | Y | `Nothing` |

### Type: `FixedSupply`
| | |
| --- | --- |
| **File** | `energy_systems/general/fixed_supply.jl` |
| **Available models** | `default` |
| **System function** | `fixed_source` |
| **Medium** | `custom` |
| **Input media** | `None` |
| **Output media** | `custom` |
| | |

Generalised implementation of a fixed source.

Must be given a profile for the energy it can provide, which is scaled by the given scale factor. If the medium supports it, it can either be given a profile for the temperature or use a static temperature.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `energy_profile_file_path` | `String` | N | `profiles/district/energy_source.prf` |
| `temperature_profile_file_path` | `String` | N | `profiles/district/temperature.prf` |
| `static_temperature` | `Temperature` | Y | `Nothing` |

### Type: GridConnection
| | |
| --- | --- |
| **File** | `energy_systems/connections/grid_connection.jl` |
| **Available models** | `default` |
| **System function** | `bounded_source`, `bounded_sink` |
| **Medium** | `custom` |
| **Input media** | `custom` (or none) |
| **Output media** | `custom` (or none) |
| | |

Used as a source or sink with no limit, which receives or gives off energy from/to outside the system boundary.

If parameter `is_source` is true, acts as a `bounded_source` with only one output connection. Otherwise a `bounded_sink` with only one input connection.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `medium` | `String` | N | `m_e_ac_230v` |
| `is_source` | `Boolean` | N | `True` |

## Other sources and sinks

### Type: PVPlant
| | |
| --- | --- |
| **File** | `energy_systems/electric_producers/pv_plant.jl` |
| **Available models** | default: `simplified` |
| **System function** | `fixed_source` |
| **Medium** | `None` |
| **Input media** | `None` |
| **Output media** | `m_el_out`/`m_e_ac_230v` |
| | |

A photovoltaic (PV) power plant producing electricity.

The energy it produces in each time step must be given as a profile, but can be scaled by a fixed value.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `energy_profile_file_path` | `String` | N | `profiles/district/pv_output.prf` |
| `scale` | `Float` | N | 4000 |

## Transformers

### Type: CHPP
| | |
| --- | --- |
| **File** | `energy_systems/electric_producers/chpp.jl` |
| **Available models** | default: `simplified` |
| **System function** | `transformer` |
| **Medium** | `None` |
| **Input media** | `m_gas_in`/`m_c_g_natgas` |
| **Output media** | `m_heat_out`/`m_h_w_ht1`, `m_el_out`/`m_e_ac_230v` |
| | |

A Combined Heat and Power Plant (CHPP) that transforms combustible gas into heat and electricity.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `power` | `Float` | N | 40000 |
| `electricity_fraction` | `Float` | Y | 0.4 |
| `min_power_fraction` | `Float` | Y | 0.2 |
| `min_run_time` | `UInt` | Y | 1800 |
| `output_temperature` | `Temperature` | Y | `nothing` |

### Type: Electrolyser
| | |
| --- | --- |
| **File** | `energy_systems/others/electrolyser.jl` |
| **Available models** | default: `simplified` |
| **System function** | `transformer` |
| **Medium** | `None` |
| **Input media** | `m_el_in`/`m_e_ac_230v` |
| **Output media** | `m_heat_out`/`m_h_w_lt1`, `m_h2_out`/`m_c_g_h2`, `m_o2_out`/`m_c_g_o2` |
| | |

Implementation of an electrolyser splitting water into hydrogen and oxygen while providing the waste heat as output.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `min_power_fraction` | `Float` | Y | 0.2 |
| `heat_fraction` | `Float` | Y | 0.4 |
| `min_run_time` | `UInt` | Y | 1800 |
| `output_temperature` | `Temperature` | Y | 55.0 |

### Type: GasBoiler
| | |
| --- | --- |
| **File** | `energy_systems/heat_producers/gas_boiler.jl` |
| **Available models** | default: `simplified` |
| **System function** | `transformer` |
| **Medium** | `None` |
| **Input media** | `m_gas_in`/`m_c_g_natgas` |
| **Output media** | `m_heat_out`/`m_h_w_ht1` |
| | |

A gas boiler that transforms combustible gas into heat.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `power` | `Float` | N | 40000 |
| `min_power_fraction` | `Float` | Y | 0.2 |
| `min_run_time` | `UInt` | Y | 1800 |
| `output_temperature` | `Temperature` | Y | `nothing` |

### Type: HeatPump
| | |
| --- | --- |
| **File** | `energy_systems/heat_producers/heat_pump.jl` |
| **Available models** | default: `carnot` |
| **System function** | `transformer` |
| **Medium** | `None` |
| **Input media** | `m_el_in`/`m_e_ac_230v`, `m_heat_in`/`m_h_w_lt1` |
| **Output media** | `m_heat_out`/`m_h_w_ht1` |
| | |

Elevates supplied low temperature heat to a higher temperature with input electricity.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `power` | `Float` | N | 40000 |
| `min_power_fraction` | `Float` | Y | 0.2 |
| `min_run_time` | `UInt` | Y | 1800 |
| `fixed_cop` | `Float` | N | 3.0 |
| `input_temperature` | `Temperature` | Y | `nothing` |
| `output_temperature` | `Temperature` | Y | `nothing` |

## Storage

### Type: Battery
| | |
| --- | --- |
| **File** | `energy_systems/storage/battery.jl` |
| **Available models** | default: `simplified` |
| **System function** | `storage` |
| **Medium** | `custom` |
| **Input media** | `custom` |
| **Output media** | `custom` |
| | |

A storage for electricity.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `medium` | `String` | N | `m_e_ac_230v` |
| `capacity` | `Float` | N | 10000 |
| `load` | `Float` | N | 5000 |

### Type: BufferTank
| | |
| --- | --- |
| **File** | `energy_systems/storage/buffer_tank.jl` |
| **Available models** | default: `simplified` |
| **System function** | `storage` |
| **Medium** | `custom` |
| **Input media** | `custom` |
| **Output media** | `custom` |
| | |

A short-term storage for heat of thermal carrier fluids, typically water.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `medium` | `String` | Y | `m_h_w_ht1` |
| `capacity` | `Float` | N | 10000 |
| `load` | `Float` | N | 5000 |
| `use_adaptive_temperature` | `Float` | Y | `False` |
| `switch_point` | `Float` | Y | 0.15 |
| `high_temperature` | `Float` | Y | 75.0 |
| `low_temperature` | `Float` | Y | 20.0 |

### Type: SeasonalThermalStorage
| | |
| --- | --- |
| **File** | `energy_systems/storage/seasonal_thermal_storage.jl` |
| **Available models** | default: `simplified` |
| **System function** | `storage` |
| **Medium** | `custom` |
| **Input media** | `m_heat_in`/`m_h_w_ht1` |
| **Output media** | `m_heat_out`/`m_h_w_lt1` |
| | |

A long-term storage for heat stored in a stratified artificial aquifer.

| Parameter | Type | Default(Y/N) | Example |
| ----------- | ------- | --- | ------------------------|
| `capacity` | `Float` | N | 1000000 |
| `load` | `Float` | N | 500000 |
| `use_adaptive_temperature` | `Float` | Y | `False` |
| `switch_point` | `Float` | Y | 0.15 |
| `high_temperature` | `Float` | Y | 75.0 |
| `low_temperature` | `Float` | Y | 20.0 |
