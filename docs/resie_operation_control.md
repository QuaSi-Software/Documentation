# Operation and control

An important part of what makes ReSiE's simulation model different from similar tools is how the control of energy system components is handled. Actualized energy systems, as they are built in real buildings, have a complex control scheme that also incorporates aspects that are not part of the model, such as hydraulic components and feed/return lines. This in turn requires that these complex control schemes can be modeled as close to reality as possible while staying inside the fundamental model of energy balances.

## The control step
Because the general calculation of energies of components might require information from other components in the energy system, particularly information that cannot be communicated across interfaces between directly connected components, it has proven beneficial to introduce a simulation step in which some information is determined and communicated before the operation of components is calculated in the `potential` and `process` steps. This step is also used to fetch information that is given as input or can otherwise be determined without any information from components.

## General mechanisms of control
Each component is assigned a controller that handles general mechanisms of control and updates any [control modules](resie_operation_control.md#control-modules) that might be attached to the component.

### Storage un-/loading flags
All components can be set to be dis-/allowed to un-/load storages to which they output or from which they draw energy. This only makes sense if an intermediary bus exists because direct connections to/from storages must always be allowed to transfer energy. The flags to control this behaviour are set in the `control_parameters` entry of the component parameter specification (compare [component specification](resie_component_parameters.md#storage-un-loading)). Similarly, components can be configured to be dis-/allowed to draw energy from storages. Any input/output not specified in this way is assumed to be allowed to un-/load storages.

### Consideration of interfaces for the potential step
Transformer components perform fairly complex calculations of their operation in the `potential` step (which is repeated in the `process` step). As part of this calculation they check how much energy is available on each of their input/output interfaces. Due to this complexity it is in rare cases necessary to specify that a particular input/output shouldn't be taken into account. This can be controlled with parameters in the `control_parameters` entry of the component configuration.

```json
{
    "uac": "TST_CHPP_01",
    "type": "CHPP",
    ...
    "control_parameters": {
        ...  
        "consider_m_el_out" : false,
    },
}
```

In the example above a CHPP is configured to not consider its electricity output for the calculations and assume the requested energy to be infinite. Any input/output not explicitly set to `false` will be considered.

## Control modules

More specialised behaviour is modeled as control modules, that can be assigned to components. The modules have predefined callbacks during specific parts of a timestep and the return values of the callbacks are aggregated across all relevant modules of the component. Because the callbacks are hardcoded into the code of a component, some modules can only be assigned to certain component types, that make use of the callbacks. **Note:** At the moment it is possible to assign any module to any component, but mismatching modules will have no effect. This may be improved in a future update.

The currently implemented callbacks are:

* `upper_plr_limit`: Sets the upper limit of the PLR to a given value. "Upper" in this case means that the PLR is calculated to not exceed this value, but it may be lower due to the exact circumstances of available energies on the inputs and outputs of a component. For example a module might set the limit to 75%, however the component is limited by available input energy and can only be operated at 50%. This callback is implemented for transformers.
* `charge_is_allowed`: Allows the charging of a battery.
* `discharge_is_allowed`: Allows the discharging of a battery.

The following described the currently implemented control modules. The required parameters are described in the [component specification chapter](resie_component_parameters.md#control-modules).

* `economical_discharge`: Handles the discharging of a battery to only be allowed if sufficient charge is available and a linked PV plant has available power below a given threshold. Mostly used for examplatory purposes.
* `profile_limited`: Sets the maximum PLR of a component to values from a profile. Used to set the operation of a component to a fixed schedule while allowing circumstances to override the schedule in favour of lower values.
* `storage_loading`: Controls a component to only operate when the charge of a linked storage component falls below a certain threshold and keep operating until a certain higher threshold is reached and minimum operation time has passed. This is often used to avoid components switching on and off rapidly to keep a storage topped up, as realised systems often operate with this kind of hysteresis behaviour.

## State machines

State machines are a [common concept](https://en.wikipedia.org/wiki/Finite-state_machine) in computer science and are useful in working with state based on predefined conditions. They have also been used in programming the building control system of actualized building. In the simulation model they are used with some modifications as described in the following.

<center>![Example of a state machine with two states](fig/example_state_machine.png)</center>

The example above shows a state machine with two states "Off" and "Fill tank" that starts in state "Off". Between the two states are transitions based on boolean expressions of complex conditions. When the state machine is checked to advance its state[^2] and the expression of a transition evaluates as true, it is followed to the new state.

One addition to the common concept of a state machine is that the implementation in ReSiE keeps track of how many steps a state machine was in the current state.

[^2]: Usually this happens once a simulation step for each state machine, but in the general definition of a state machine this is not time-dependant and works on "turns".

### Conditions

The conditions used in evaluating the boolean expressions of transitions are arbitrarily complex and as such depend on the implementation. However the code handling them must define which information it requires for evaluation. In particular a condition must define to which components it needs access. As the specific components are not defined before the project is loaded, these requirements affect the type and possibly the medium of the components, e.g. a condition might ask for "a grid connection of medium m_e_ac_230v" or "a PV plant". It can also provide customizable parameters with default values.

The example above uses three different conditions:

* `BT >= X%`: Checks if a linked buffer tank is above X% capacity.
* `BT < X%`: Checks if a linked buffer tank is below X% capacity.
* `Min. run time`: Checks if the component the state machine controls has been in the current state for longer or equal than its minimum run time.

To make sure that the buffer tank is not overfilled, the component linked to this buffer checks this condition itself during each timestep by comparing the free storage space and the possible energy that could be delivered to the buffer tank while considering the minimum partial load of the component. Therefore, this condition is not included in the state machine.  

### Truth table

The transitions for each state are defined using a truth table over the conditions involved, resulting in a new state (which may result in the current state again). This has the advantage that is covers every possible case implicitly, but also has the disadvantage that this might result in large truth tables for state machines with many conditions.

| **BT >= X%** | **Min. run time** | **New state** | 
| --- | --- | --- |
| true | true | Off |
| false | true | Fill tank |
| true | false | Fill tank |
| false | false | Fill tank |

The example above shows the truth table used for the state "Fill tank", which has two conditions. In this case, the buffer tank should be filled exept of the case where both the minimum run time has reached and the buffer tanks is filled above the defined upper load state. The condition to not overfill the buffer tank is handled by each component during each time step and not by the state machine.
