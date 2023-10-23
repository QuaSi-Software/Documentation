# GenSim user manual
## **1  What is GenSim?**

GenSim - for "generic building simulation" - is a building simulation software using the *EnergyPlus®* simulation computing core to generate high-resolution heating and cooling demand profiles as well as electricity demand profiles and PV outputs. "Generic" in this context means "generally valid" building model. This means that the software can be used to model and simulate any type of building in a very flexible and simplified way. 
The software was developed for use in the context of project pre-planning where usually no large time budget is available for detailed simulations of buildings. A detailed input and simulation of buildings with common applications like *DesignBuilder®*, *IDA ICE®* or *TRNSYS®* is usually time consuming. GenSim was therefore developed with the aim of ensuring the fastest and simplest possible simulation of buildings. In early planning phases often only relatively rough data on the planned buildings are available. Therefore an optimal relationship between the level of detail of the model and the accuracy of the input parameters should be achieved. 

The input and output of the software is based on *Microsoft Excel®*. The computing core, based on *OpenStudio®*[^1] and *EnergyPlus®*, is connected to the Excel interface via Visual Basic for Applications® - see following figure. 

[^1]: OpenStudio® provides a development environment for the individual use of EnergyPlus® in software applications.  

![simplified software structure](fig\231023_simplified_software_structure.PNG)

The basis is formed by a standardized (generic) building model, which has all the essential levels of freedom or basic functions in order to be able to represent any type of building. These basic functions (see following figure) can be adjusted by a few simple parameters. Details on the individual basic functions and their parameters will follow in chapter 3. 
An exception is the possibility besides the generic geometry generation (cubic building) to create the geometry model individually using the OpenStudio SketchUp plugin and then import it into GenSim. 

![basic functions of the standardized building model](fig\231023_basic_functions_building_model.PNG)

The main result of GenSim are temporally high-resolution profiles in units of  \(Wh/m²_{NRF}\). Within the building simulation no distribution or transfer losses are represented. Therefore all results have t be evaluated as net energies. Distribution losses must be imprinted in the aftermath itself for example in the form of an offset. 

In addition to the output profiles GenSim offers various annual values, an overview of the building balance and the possibility of sensitivity analyses (see following figure). 

GRAFIK EINFÜGEN




## **2  Installation**

*Content coming soon*

## **3  Model functions and parameters**
###3.1 Location

Starting the modeling on the homepage of the GenSim Excel interface with the selection of the location.


![selection of the weather data in Excel](fig\231023_selection_weather_data.png)

For the 25 largest german cities corresponding EnergyPlus weather datasets[^2] were generated using the current DWD test reference years (TRY 2015/2045). 
[^2]: File format "epw" - EnergyPlus weather data