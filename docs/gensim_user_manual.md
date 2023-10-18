# GenSim user manual
**1  What is GenSim?**

GenSim - for "generic building simulation" - is a building simulation software using the *EnergyPlus®* simulation computing core to generate high-resolution heating and cooling demand profiles as well as electricity demand profiles and PV outputs. "Generic" in this context means "generally valid" building model. This means that the software can be used to model and simulate any type of building in a very flexible and simplified way. 
The software was developed for use in the context of project pre-planning where usually no large time budget is available for detailed simulations of buildings. A detailed input and simulation of buildings with common applications like DesignBuilder®, IDA ICE® or TRNSYS® is usually time consuming. GenSim was therefore developed with the aim of ensuring the fastest and simplest possible simulation of buildings. In early planning phases often only relatively rough data on the planned buildings are available. Therefore an optimal relationship between the level of detail of the model and the accuracy of the input parameters should be achieved. 


**2  Installation**

*Content coming soon*

1. Get a copy: `git clone git@github.com:QuaSi-Software/resie.git`
1. Switch into project directory: `cd /path/to/repo`
1. Start the julia REPL with `julia`
1. Switch to the package REPL with `]` (no enter necessary)
1. Activate the project environment: `activate .`
1. Add required packages: `add ColorSchemes Debugger Infiltrator JSON PlotlyJS ResumableFunctions Test`
1. Exit out of the package REPL with shortcut `Ctrl+c`
1. Exit out of the julia REPL with `exit()`

![General System chart of a heat pump](fig/221018_HeatPump_system_chart.svg)
