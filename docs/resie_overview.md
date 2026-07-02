# What is ReSiE?

ReSiE is a simulation engine for the analysis of energy supply systems in multi-sectoral district-scale projects. It is used to simulate the power, heat and general energy flow between energy system components, such as heat pumps, PV installations or ground-coupled heat storages. ReSiE also allows for economical analysis of results, calculation of GHG emissions and offers options for black-box optimisation. The name is derived from *Rechenkern für die Simulation von Energiesystemen* in German, meaning *calculation engine for the simulation of energy systems*.

## Purpose and scope

The main use case of ReSiE is aiding the creation and evaluation of concepts for the energy supply system of buildings and districts in the early planning stage of construction and renovation projects. At such a stage only limited information is available, yet decisions on the energy system have to be made, that are carried forward into more advanced planning stages where more details have to be considered. ReSiE aims to facilitate a workflow that transitions from these early to later stages.

The engine implements a novel mathematical approach based on aspects of systems analysis, agent-based simulation and graph theory, which can cover non-linear control mechanisms and imposes no limit on the complexity of component models. Compared to other available open source tools, commonly using a linear optimisation or MILP approach, ReSiE offers far more flexibility in what you can model and simulate with the tool and in how much detail. However this comes at the cost that optimisation is slow and can only work with black-box optimisation algorithms. It is thus less useful, compared to such other tools, to quickly find the right sizing of all components of a complex energy system.

ReSiE calculates the energy that flows between components based on the demands and available energy sources in each time step, taking into account which constraints the connections between them impose. Temperatures are considered where necessary to calculate an amount of energy, however mass flow and the hydraulic system in general is not modeled directly. Where the energy balance cannot be maintained, this is also an output of the simulation, as this is important information on the operation of the energy system.

## Next steps
- more info on simulation method and input file
- installation
- examples
- UI tools SIMON and SUSI