# GenSim user manual
## **1  What is GenSim?**

GenSim - for "generic building simulation" - is a building simulation software using the *EnergyPlus®* simulation computing core to generate high-resolution heating and cooling demand profiles as well as electricity demand profiles and PV outputs. "Generic" in this context means "generally valid" building model. This means that the software can be used to model and simulate any type of building in a very flexible and simplified way. 
The software was developed for use in the context of project pre-planning where usually no large time budget is available for detailed simulations of buildings. A detailed input and simulation of buildings with common applications like *DesignBuilder®*, *IDA ICE®* or *TRNSYS®* is usually time consuming. GenSim was therefore developed with the aim of ensuring the fastest and simplest possible simulation of buildings. In early planning phases often only relatively rough data on the planned buildings are available. Therefore an optimal relationship between the level of detail of the model and the accuracy of the input parameters should be achieved. 

The input and output of the software is based on *Microsoft Excel®*. The computing core, based on *OpenStudio®*[^1] and *EnergyPlus®* is connected to the Excel interface via Visual Basic for *Applications®* - see following figure. 

[^1]: OpenStudio® provides a development environment for customised use of EnergyPlus® in software applications. 

![simplified software structure](fig\231023_simplified_software_structure.PNG)

The basis is a standardised (generic) building model that has all the essential levels of freedom or basic functions in order to be able to represent any type of building. These basic functions (see figure below) can be adjusted by a few simple parameters. Details of the individual basic functions and their parameters are given in chapter 3. 
An exception is the possibility besides the generic geometry generation (cubic building) to create a custom geometry model using the OpenStudio SketchUp plugin and then import it into GenSim. 

![basic functions of the standardized building model](fig\231023_basic_functions_building_model.PNG)

The main output of GenSim is high-resolution profiles in units of  \(Wh/m²_{NRF}\). Within the building simulation no distribution or transfer losses are represented. Therefore all results must be evaluated as net energy. Distribution losses must be imprinted afterwards for example in the form of an offset. 

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
In general any *EnergyPlus®* weather data set can be stored by the user and selected for the simulation with GenSim. A complete weather data set always consists of an epw-file and a ddy-file which must be stored under the same file name in the subfolder "weather" in the GenSim file path. The refresh button can be used to update the selection in the drop down list.
Ready-to-use weather datasets (epw + ddy) for worldwide locations can be downloaded free of charge from the following websites: 

[https://energyplus.net/weather](https://energyplus.net/weather)    
[http://climate.onebuilding.org/](http://climate.onebuilding.org/) 


Furthermore the TRY of the DWD can be used to generate location-specific weather data sets for the whole of Germany which can then be converted into valid EnergyPlus weather data sets using the "EnergyPlus Weather Converter". For this purpose a separate and more detailed instruction can be found in the following folder path:

*Verweis auf interne Dokumente*


###3.2 Building geometry

The building geometry can be defined in two ways. Either a generic cubic geometry model can be parameterised or the geometry can be individually created and imported. The choice between these two options is made using a drop down menu (see the following figure). Both options are described below. 

![selection of the method for geometry generation in the Excel® GUI](fig\231023_selection_method.png)

Basically the *EnergyPlus®* geometry model is illustrated with its external dimensions but no component thicknesses or volumes (e.g. wall or ceiling thicknesses) are represented. As a result the entire Gross Floor Area (BGF) or Gross Room Volume (BRF) is simulated as the volume to be conditioned. The inaccuracy resulting from this simplification is negligible in any case given the low level of model detail. The net room area (NRF) is used to convert the results into area-specific quantities. This means that the absolute results of the simulation are related to a typical NRF corresponding to the simulated BGF.

####3.2.1 Generic building model

The generic geometry model is a cubic building (see figure) defined by the parameters "length", "width", " height", "number of floors" and "window area proportions"[^5] (see figure). An idealised floor plan is used which divides each floor into 4 external zones and one internal zone (see figure). 

After the simulation it is possible to view the generic geometry model in *SketchUp®* using the *OpenStudio®* SketchUp plug-ins. The model file is located in 
"/Output/run" directory under the name "in.osm".
[^5]: Ratio of transparent to opaque outer surface 

![generic geometry model](fig\231023_generic_geometric_model.png)

![generic geometry model - floor plan](fig\231023_generic_model.png)


**Measurements**

The "length" and "width" of the building are indicated as external dimensions. It is the length of the north-south facing facade and the width of the east-west facing facade (see figure above). The “floor height" is specified as the gross floor height. The multiplication of "floor height" and "number of floors" results in the total height of the building. The parameter "depth outer zones" additionally defines the depth of the outer zones[^6] according to the figure above. 
[^6]: An outer zone with a depth of 0m results in a one-zone model

![definition geometry model](fig\231025_definition_geometry_model.PNG)


**Orientation**

The orientation of the building can also be changed using a drop down menu (see following figure) if the building should not lie exactly in the axes of the main cardinal points. A positive rotation of the building corresponds to a clockwise rotation[^7].
[^7]: See EnergyPlus® parameter "north axis": [https://bigladdersoftware.com](https://bigladdersoftware.com/epx/docs/8-0/input-output-reference/page-006.html#field-north-axis)    

![definition orientation](fig\231025_definition_orientation.png)



**NRF/BGF ratio**

As already mentioned only gross areas or volumes are represented in the EnergyPlus® model. In order to convert the absolute results of the simulation into area specific results with the unit \(Wh/m²_{NRF}\) the user now needs to specify the ratio BGF/NRF. This can either be entered as an individual value or it can be determined from previously stored characteristic values. Key figures from the Building Cost Index (BKI) and VDI 3807-2 have been stored for a variety of building typologies. 


**Window areas**

Besides the actual geometry window areas also need to be defined. Therefore a corresponding "window band"[^8] is modelled by specifying a proportion of window area per facade (m² of window area / m² of facade area [%] - see following figure).
[^8]: Ratio of transparent to opaque outer surface (window without frame) 

![window area](fig\231025_window_area.PNG)


**Adiabatic external components**

Optionally individual facade components as well as the roof and floor plate of the building can be defined as adiabatic. Adiabatic means that the component does not allow heat transfer. This makes it possible e.g. to simulate coupled terraced houses or any other sub-volume of a whole building by defining component boundaries to heated zones as adiabatic. The procedure for the imported geometry model is explained in more detail in Section 3.2.4 Adiabatic External Components below. 



####3.2.2 Imported geometry model

As already mentioned an individual geometry model can optionally be created with the OpenStudio® SketchUp® plugin if the building geometry is known in more detail and/or  significantly differs from a cubic shape. The osm-model file created this way can be imported into GenSim by the Import button (see following figure). A short tutorial on how to create your own geometry model can be found in the following section 5. Currently the gross floor area (GFA) of the imported OpenStudio® model is not read in automatically so the user must enter it manually. If required, the actual GFA of the model can be read from the file "eplustbl.htm" in the "/Output/run" file path after a test simulation run (Total Building Area). The (gross) floor height of the imported geometry model itself must also be entered. 


*figure missing*


###3.3 Building usage

By using electrical devices the user directly influences the electricity demand. In addition the usage of the building also has a significant impact on the heating and cooling demand in the form of internal heat loads from electrical devices and lighting as well as heat emitted by the people present. The internal heat loads of these 3 groups are basically defined by two components. On the one hand by load profiles and on the other hand by defining power densities and occupancy densities. The load profiles are defined in the form of type days for working days, Saturdays and Sundays (see following figure). In addition it is possible to define individual time periods for public holidays/vacation days as well as an additional type day for public holidays/vacation days. Depending on the parameter "first day of the year" an annual profile is generated on the basis of the individual type day profiles. 

![parameter first day of the year](fig\231025_parameter_first_day.png)

*figure missing*

Up to 5 periods can be defined for public holidays/vacation days (see following figure). These can be holiday periods e.g. when simulating a school or university building.

![definition of holidays/ vacation days](fig\231025_definition_holidays.PNG)


**Electrical devices and lightning**

The type days for electrical devices and lighting are available in the form of standardised profiles. The range of values is therefore between 0 ... 1. Multiplying the corresponding power density in \(W/m²_{NRF}\) and the type day profile results in a profile in \(W/m²_{NRF}\). See the following figure: "Electrical devices" and "Lighting" drop-down menus as well as the "Electrical device power density" and "Lighting power density" parameters. 

**Person occupancy**

Two separate type day profiles are defined for person occupancy. On the one hand a standardised profile describing the presence of persons (0...1) and on the other hand a profile describing the activity of the persons present in the unit power per person \(W/pers\). 

![definition of the building usage](fig\231025_definition_building_usage.PNG)
