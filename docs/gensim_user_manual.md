# GenSim user manual
## **1  What is GenSim?**

GenSim - for "generic building simulation" - is a building simulation software using the *EnergyPlus®* simulation computing core to generate high-resolution heating and cooling demand profiles as well as electricity demand profiles and PV outputs. "Generic" in this context means "generally valid" building model. This means that the software can be used to model and simulate any type of building in a very flexible and simplified way. 
The software was developed for use in the context of project pre-planning where usually no large time budget is available for detailed simulations of buildings. A detailed input and simulation of buildings with common applications like *DesignBuilder®*, *IDA ICE®* or *TRNSYS®* is usually time consuming. GenSim was therefore developed with the aim of ensuring the fastest and simplest possible simulation of buildings. In early planning phases often only relatively rough data on the planned buildings are available. Therefore an optimal relationship between the level of detail of the model and the accuracy of the input parameters should be achieved. 

The input and output of the software is based on *Microsoft Excel®*. The computing core, based on *OpenStudio®*[^1] and *EnergyPlus®*, is connected to the Excel interface via Visual Basic for Applications® - see following figure. 

[^1]: OpenStudio® provides a development environment for customised use of EnergyPlus® in software applications. 

![simplified software structure](fig\231023_simplified_software_structure.PNG)

The basis is a standardised (generic) building model that has all the essential levels of freedom or basic functions in order to be able to represent any type of building. These basic functions (see figure below) can be adjusted by a few simple parameters. Details of the individual basic functions and their parameters are given in chapter 3. 
An exception is the possibility besides the generic geometry generation (cubic building) to create a custom geometry model using the OpenStudio SketchUp plugin and then import it into GenSim. 

![basic functions of the standardized building model](fig\231023_basic_functions_building_model.PNG)

The main output of GenSim is high-resolution profiles in units of  \(Wh/m²_{NRF}\). Within the building simulation no distribution or transfer losses are represented. Therefore all results must be evaluated as net energy. Distribution losses must be imprinted in the aftermath itself for example in the form of an offset. 

In addition to the output profiles GenSim provides various annual values, an overview of the building balance and the ability to perform of sensitivity analyses (see  figure below). 

![overview of the output sizes](fig\231023_overview.PNG)



## **2  Installation**

*Content coming soon*

## **3  Model functions and parameters**
###3.1 Location

The modelling process starts on the homepage of the GenSim Excel interface with the selection of the location.


![selection of the weather data in Excel](fig\231023_selection_weather_data.png)

Corresponding *EnergyPlus®* weather datasets[^2] have been generated for the 25 largest German cities using the current DWD test reference years (TRY 2015/2045). Both the current TRY2015[^3] and the future scenario TRY2045[^4] have been stored in order to be able to consider the climatic requirements for heating, air conditioning and ventilation systems over a longer period of operation. The required weather data set can be selected from a drop down list. 

[^2]: File format "epw" - EnergyPlus weather data
[^3]: Reference period 1995 to 2012
[^4]: Forecast period 2031 to 2060

**Store and simulate custom weather data sets**
In general any *EnergyPlus®* weather data set can be stored by the user and selected for the simulation with GenSim. A complete weather data set always consists of an epw-file and a ddy-file, which must be stored under the same file name in the subfolder "weather" in the GenSim file path. The refresh button can be used to update the selection in the drop down list.
Ready-to-use weather datasets (epw + ddy) for worldwide locations can be downloaded free of charge from the following websites: 

[https://energyplus.net/weather](https://energyplus.net/weather)    
[http://climate.onebuilding.org/](http://climate.onebuilding.org/) 


Furthermore the TRY of the DWD can be used to generate location-specific weather data sets for the whole of Germany which can then be converted into valid EnergyPlus weather data sets using the EnergyPlus Weather Converter. For this purpose, a separate and more detailed instruction can be found in the following folder path:

*Verweis auf interne Dokumente*


###3.2 Building geometry

The building geometry can be defined in two ways. Either a generic cubic geometry model can be parameterised, or the geometry can be individually created and imported. The choice between these two options is made using a drop down menu (see the following figure). Both options are described below. 

![selection of the method for geometry generation in the Excel® GUI](fig\231023_selection_method.png)

Basically the *EnergyPlus®* geometry model is illustrated with its external dimensions but no component thicknesses or volumes (e.g. wall or ceiling thicknesses) are represented. As a result the entire Gross Floor Area (BGF) or Gross Room Volume (BRF) is simulated as the volume to be conditioned. The inaccuracy resulting from this simplification is negligible in any case given the low level of model detail. The net room area (NRF) is used to convert the results into area-specific quantities. This means that the absolute results of the simulation are related to a typical NRF corresponding to the simulated BGF.

####3.2.1 Generic building model

The generic geometry model is a cubic building (see figure) defined by the parameters "length", "width", " height", "number of stores" and "window area proportions"[^5] (see figure). An idealised floor plan is used which divides each floor into 4 external zones and one internal zone (see figure). 

After the simulation it is possible to view the generic geometry model in *SketchUp®* using the *OpenStudio®* SketchUp plug-ins. The model file is located in 
"/Output/run" directory under the name "in.osm".
[^5]: Ratio of transparent to opaque outer surface 

![generic geometry model](fig\231023_generic_geometric_model.png)

![generic geometry model - floor plan](fig\231023_generic_model.png)

**Measurements**

*Content coming soon*