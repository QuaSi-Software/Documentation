# Examples

In this chapter, some exemplary energy systems will be described and discussed. This may help to understand the capabilities, limitations and usage of ReSiE.

For all examples the required input files are shipped together with ReSiE as JSON files in the [subdirectory `examples`](https://github.com/QuaSi-Software/resie/tree/master/examples). The project files may link to profile files (as `.prf`), which are also shipped alongside ReSiE in the [`profiles` subdirectory](https://github.com/QuaSi-Software/resie/tree/master/profiles). The examples can be executed with

```bash
julia --project=. src/resie-cli.jl run --exit-after-run examples/name_of_example.json
```

in the ReSiE directory. More information on how to use the CLI can be found [in this chapter](resie_installation.md). The outputs are written to the `output` subdirectory by default. Please note that output files from multiple simulation runs (including different examples) are not deleted, but are overwritten.

All examples will produce an interactive plot of interesting result data (default `output/output_plot.html`) and a sankey plot of yearly sums of energy (default `output/output_sankey.html`). You can customize both plots as described in [the chapter on the input file format](resie_input_file_format.md). The log files (default `output/logfile_general.log` and `output/logfile_balanceWarn.log`) are of interest as well, particularly if the example generates warnings on purpose.

## Minimal example of a heat pump
![Simple heat pump energy system](fig/examples/240410_simple_heat_pump.svg)

File: [`examples/simple_heat_pump.json`](https://github.com/QuaSi-Software/resie/tree/master/examples)

A fairly minimal example of operating a heat pump to supply a heat demand by using electricity from the grid and a heat source. The heat source provides temperatures in the range of 19 °C to 27 °C. The demand takes in heat at temperatures varying from 49 °C to 66 °C. The heat pump works with a fixed COP of 3.0.

This example demonstrates how an energy system with a heat pump can be structured on a basic level. Heat pumps are an important and versatile component, however also provide some modelling challenges in combination with other components that handle heat in a complex way. Therefore this example is a known baseline from which energy systems using a heat pump can extend.

For a slightly more advanced version you can change the line `"cop_function": "const:3.0"` from the subconfig of the heat pump to `"cop_function": "carnot:0.4"`. The varying temperatures of input and output are then considered in a simplified Carnot-efficiency calculation and result in a dynamic COP.

## Heating and cooling demands
![Heating and cooling demands in one energy system](fig/examples/240610_heating_and_cooling.svg)

File: [`examples/heating_and_cooling.json`](https://github.com/QuaSi-Software/resie/tree/master/examples)

In this example a heating and a cooling demand are satisfied by making use of the low temperature heat as the source for the heat pump supplying high temperature heat, while only the excess is removed as waste heat. The excess is elevated to a higher level so that heat exchangers can effectively remove the heat from the system. This demonstrates that a cooling demand is in fact a heat source in disguise and can be modelled as a fixed supply of low temperature heat.

There is no additional heat supplier in the system, which is only possible as the cooling demand has a fairly high base load all the time and a heat storage is used to buffer peaks. This could model an office building which, in addition to room cooling, also produces waste heat from a cluster of servers.

The heat pumps works on multiple temperature layer, resulting in different COPs for different combinations of input and output temperatures. The heat pump 1 can cover the demand directly, or load the the buffer tank on a higher temperature, or both is done within the same timestep. This results in a mean COP and mean output temperature over the whole timestep. The defined prioritization (usable energy of heat pump 1 has a higher priority as heat pump 2) works as expected.

## Multi-family house including economy and GHG emissions

![Multi-family house energy system: overview](fig/examples/260610_multi_family_house.svg)

File: [`examples/multi_family_house.json`](https://github.com/QuaSi-Software/resie/tree/master/examples)

This example represents the energy system of a multi-family house with electricity, space heating and domestic hot water demands. In this first example, a single configuration of the components is simulated and described. Further below in [this chapter](resie_exemplary_energy_systems.md/#optimisation-and-sensitivity-analysis-of-the-multi-family-house), an optimisation of the component sizing and a sensitivity analysis is shown. 

In this example, electricity is supplied by a photovoltaic plant, a battery and the public electricity grid, where the battery is not allowed to take energy from or deliver energy to the grid. Heat is supplied by an air-source heat pump using ambient air as a heat source. Two buffer tanks are used to separate space heating and domestic hot water at different temperature levels. The connections from the hotter domestic hot water buffer tank to the colder heating buffer tankW and the heating demand are disabled, as ReSiE automatically cools down thermal energy and would therefore transfer energy between these components. The connections from the heating buffer tank to the DHW demand and the DHW buffer tank can be allowed, as the temperature is lower and no energy will be delivered. 

The heat pump is modelled as an inverter heat pump with a Carnot-based COP, part-load dependencies, icing behaviour and losses. It supplies heat at two different temperature levels through one heat output interface and one shared thermal bus, in order to serve the thermal energy for space heating at a lower temperature than for domestic hot water. This improves the COP compared to supplying all heat at the higher domestic hot water temperature level.

The example demonstrates a building-scale sector-coupled system including local electricity generation, electrical storage, grid exchange and heat pump operation. Surplus PV electricity can be used by the demands, stored in the battery or exported to the grid. Remaining electricity demand is supplied by the grid.

The resulting energy-flow Sankey plot can be seen here:

![Multi-family house energy system: Sankey plot](fig/examples/260610_multi_family_house_sankey.png)

A particular focus of this example is the combined evaluation of operation, economy and greenhouse gas emissions over an observation period of 20 years. Grid electricity uses dynamic price and emission profiles for Germany in 2024, while exported electricity receives a constant feed-in price. In addition to the standard result plots, the example produces economic cashflow and present value plots as well as emission plots and CSV outputs.

In the economic evaluation, this example is mainly interpreted from the perspective of the building owner, as internal electricity and heat demands are not assigned energy prices, while investment costs, grid electricity costs and feed-in revenues are considered:

![Multi-family house energy system: economic results](fig/examples/260610_multi_family_house_economy.png)

The GHG emissions are modelled without emission credits and without embodied emissions. Grid electricity as the only GHG emission uses a dynamic, hourly emission profile with a yearly change rate:

![Multi-family house energy system: emission results](fig/examples/260610_multi_family_house_emissions.png)

The example can be used to investigate the influence of PV and battery sizing, heat pump operation, temperature levels, dynamic electricity prices and grid emission factors on self-consumption, grid exchange, operational costs and GHG emissions.

## District with river-water heat pump including economy and GHG emissions

![District energy system with river-water heat pump: overview](fig/examples/260610_river-water_district.svg)

File: [`examples/river_water_district.json`](https://github.com/QuaSi-Software/resie/tree/master/examples)

This example represents a small district with two buildings, photovoltaic plants, electricity demands, space heating demands and domestic hot water demands. The buildings are connected to a central electricity bus and a central thermal bus. Heat is supplied by a river-water heat pump, a central buffer tank and a gas boiler for peak load coverage. The central battery is not allowed to take energy from or deliver energy to the grid.

The example demonstrates how central and decentral structures can be combined in one energy system. Heat is distributed from the central thermal bus to both buildings at a comparatively low temperature level for space heating. Domestic hot water is prepared locally in each building by using thermal boosters, which raise the temperature only where the higher domestic hot water temperature is required. This reduces the temperature level of the central heat supply and can improve the operation of the heat pump.

On the electrical side, the PV plants of both buildings, a central battery, grid import and grid export are connected to one central electricity bus. The locally generated electricity can supply the building electricity demands, the thermal boosters, the river-water heat pump and the battery. Remaining electricity demand is supplied by the grid, while excess electricity can be exported.

The resulting energy-flow Sankey plot can be seen here:

![District energy system with river-water heat pump: Sankey plot](fig/examples/260610_river-water_district_sankey.png)

A particular focus of this example is the combined evaluation of operation, economy and greenhouse gas emissions over an observation period of 20 years. Electricity imports use dynamic price and emission profiles for Germany in 2024, exported electricity receives a constant feed-in price and natural gas is modelled with yearly changing  price and emission assumptions. In addition to the standard result plots, the example produces economic cashflow and present value plots, emission plots, price and emission profile plots and CSV outputs.

In the economic evaluation, this example is mainly interpreted from the perspective of an integrated district energy operator. Electricity and heat supplied to the buildings are modelled as revenues, while grid electricity, natural gas, investment costs, maintenance and repair are modelled as expenses. In the results, a return of invest after 6 years can be observed:

![District energy system with river-water heat pump: economic results](fig/examples/260610_river-water_district_economy.png)

The emissions are modelled without embodied emissions. Emission credits are accounted for feed-in of unused PV electricity. Grid electricity and natural gas use dynamic emission profiles:

![District energy system with river-water heat pump: emission results](fig/examples/260610_river-water_district_emissions.png)

The example can be used to investigate the interaction between central PV and battery operation, dynamic electricity prices, a river-water heat pump, fossil peak load coverage, local domestic hot water boosting, grid exchange, operating costs and time-dependent greenhouse gas emissions.

## District with sector coupling
![Complex district energy system with multiple sectors](fig/examples/240411_multisector_district.svg)

File: [`examples/multisector_district.json`](https://github.com/QuaSi-Software/resie/tree/master/examples)

This example demonstrates complex behaviour of an energy system covering multiple sectors over the span of a year. Heating and electricity demands in two different subdivisons (e.g. for two groups of buildings) are supplied with a variety of producers. Interesting components include a hydrogen electrolyser feeding into a hydrogen grid and a seasonal thermal energy storage.

This example is also discussed in depth in Ott2023[^Ott2023], however the results discussed in the publication are based on the simplified component models from the time of publication. The example file in the ReSiE repository will use the currently implemented models, therefore results differ.

The following figure shows a sankey plot of the yearly sums of energy. All components play a role in the operation of the energy system to different degrees, which can be seen by following the flow of energy in the plot.

![Sankey plot of yearly sums of energy](fig/examples/260421_multisector_district_sankey.png)

The example has also been set up in a specific way such that the energy balance is not upheld in every time step. Distributed over the span of the two heating periods at the beginning and end of the year, the heating demand 2 is not fully met. This can happen because there is no source of heat in the energy system which can produce an arbitrary amount of heat without possibly being limited by an input or output. The CHP comes close, but fails to cover peaks in demand when the buffer tanks are empty as it is not sufficiently sized for peak load coverage. The gas boiler does act as peak load supplier, but is connected only to heating demand 1.

[^Ott2023]: Ott, E.; Steinacker, H.; Stickel, M.; Kley, C. and Fisch, M.N.: Dynamic open-source simulation engine for generic modeling of district-scale energy systems with focus on sector coupling and complex operational strategies, 2023, Journal of Physics: Conference Series 2600, 022009


## Optimisation and sensitivity analysis of the multi-family house

![Multi-family house energy system: overview](fig/examples/260610_multi_family_house.svg)

File: [`examples/multi_family_house_optim.json`](https://github.com/QuaSi-Software/resie/tree/master/examples)

This example extends the [multi-family house including economy and GHG emissions](#multi-family-house-including-economy-and-ghg-emissions) with parameter variation, component-size optimisation, and global and local sensitivity analyses. The PV scale, battery capacity, heat-pump power and space-heating buffer volume are varied, while the total annuity is minimised.

### Running and modifying the example

Parameter-study simulations can be distributed across multiple Julia threads:

```bash
julia --threads=auto --project=. src/resie-cli.jl run --exit-after-run examples/multi_family_house_optim.json
```

Replace `auto` with a fixed thread count, such as `16`, if required.

The example uses a 60-minute time step. For initial experiments, the runtime can be reduced by using a 120-minute time step, fewer optimisation runs and looser convergence tolerances for the decision variables, for example `x_tol_abs: 0.01`, and the objective function, for example `f_tol_abs: 500`. The sensitivity analyses can also be disabled during these initial tests. 

The configured parameter ranges are:

| Parameter                        | Start value | Investigated range |
| -------------------------------- | ----------: | -----------------: |
| space-heating buffer-tank volume |      2.0 m³ |        0 to 3.0 m³ |
| PV scale                         |         500 |          0 to 1000 |
| battery capacity                 |   59.38 kWh |       0 to 200 kWh |
| heat-pump thermal power          |       85 kW |        0 to 150 kW |

Predefined parameter ranges are also included for optional parameter variation as an alternative to optimization. With the `product` algorithm, four values per parameter result in 256 combinations, whereas optimisation searches continuously within the bounds.

### Using unmet-energy costs for sizing

Without a penalty for unmet demand, an optimisation could favour inexpensive but undersized components. This example therefore assigns a high unmet-energy price to the electricity and space-heating demands. Insufficient designs remain valid simulation results, but their penalty costs increase the objective and make them unattractive to the optimiser.

The price acts as a soft constraint rather than a strict feasibility condition. It should be high enough to prevent undersizing and must be assigned to every demand whose complete coverage is required. The final design should nevertheless be checked for unmet energy in a detailed single simulation.

### Optimisation

The population-based `ECA` algorithm from `Metaheuristics` performs the global search, followed by an `LN_NELDERMEAD` refinement from `NLopt`. The convergence plot contains 358 optimisation evaluations followed by 100 runs used for global sensitivity analysis while local-sensitivity runs are excluded in the plots.

<div style="margin-bottom: -1rem;">
    <iframe
        src="../fig/examples/260731_parameter_study_plots_convergence.html"
        title="Convergence of the multi-family house optimisation"
        loading="lazy"
        style="width: 100%; height: 400px; border: 0;"
    ></iframe>
</div>

[Open the convergence plot in a separate page](fig/examples/260731_parameter_study_plots_convergence.html)

The large objective values mainly represent undersized systems with unmet-energy penalties. As the search progresses, ReSiE finds matching component sizes, and the refinement explores the region around the best global result. You can zoom into the plot by holding down the mouse button and dragging a rectangle around the lower-cost region of interest.

For this example, the best evaluated design is approximately:

| Parameter                        |     Result |
| -------------------------------- | ---------: |
| space-heating buffer-tank volume |    2.90 m³ |
| PV scale                         |       1000 |
| battery capacity                 |  159.3 kWh |
| heat-pump thermal power          |    66.5 kW |
| total annuity                    | 27,512 €/a |

The PV scale reaches its upper bound, suggesting that a larger permitted PV system could be investigated. Because the global algorithm is stochastic, repeated runs may return slightly different results.

### Exploring alternative designs

An optimisation produces many evaluated designs in addition to the reported best result. The parallel-coordinates plot provides a useful overview of these alternatives:

<div style="width: 100%; height: 600px; overflow: hidden; margin-bottom: 0rem;">
    <iframe
        src="../fig/examples/260731_parameter_study_plots_parallel_coordinates.html"
        title="Parallel-coordinates plot of the multi-family house parameter study"
        loading="lazy"
        style="
            width: calc(100% / 0.85);
            height: calc(600px / 0.85);
            border: 0;
            transform: scale(0.85);
            transform-origin: top left;
        "
    ></iframe>
</div>

[Open the parallel-coordinates plot in a separate page](fig/examples/260731_parameter_study_plots_parallel_coordinates.html)

Each line represents one simulation and connects its parameter values with the resulting objective. Because unmet-energy penalties produce very high objective values for some designs, first select the economically relevant range on the objective axis and choose **Zoom to selection**. The remaining lines show which parameter combinations produced favourable results. Narrow ranges on an axis indicate similar values among these designs, while broad ranges indicate greater flexibility.

Useful other outputs of ReSiE are these additional interactive HTML plots that can be used to evaluate the path of the optimiser and the result further:

* [parameter matrix](fig/examples/260731_parameter_study_plots_matrix_plot.html), for inspecting parameter distributions and pairwise relationships
* [objective-parameter explorer](fig/examples/260731_parameter_study_plots_objective_parameter_explorer.html), for selecting and comparing individual parameters or results
* [interactive 3D plot](fig/examples/260731_parameter_study_plots_interactive_3d.html), for displaying three selected quantities and colouring the points by another result

### Sensitivity analysis

After optimisation, this example performs a sensitivity analysis. Global sensitivity identifies which parameters control the results over the complete investigated space. Local sensitivity shows how the objective responds near the selected design.

The **global sensitivity** analysis reuses the available optimisation results and performs additional simulations where required. The first-order Sobol index represents the independent contribution of a parameter, while the total-order index also includes interactions.

<div style="margin-bottom: -1rem;">
    <iframe
        src="../fig/examples/260731_parameter_study_plots_global_sensitivity.html"
        title="Global sensitivity of the multi-family house parameter study"
        loading="lazy"
        style="width: 100%; height: 750px; border: 0;"
    ></iframe>
</div>

[Open the global-sensitivity plot in a separate page](fig/examples/260731_parameter_study_plots_global_sensitivity.html)

Heat-pump power dominates the objective variation, with first- and total-order indices of approximately 92.7 % and 97.3 %. This is mainly caused by the transition between undersized systems with high unmet-energy costs and systems that can satisfy the heat demand. The other parameters therefore appear less influential over the selected ranges.

The **local sensitivity** analysis starts from the best optimisation result and changes one parameter at a time by 10 %. It shows that:

* reducing the heat-pump power by 10 % increases the objective by approximately 1867 %, while increasing it raises the objective by only about 2.2 %;
* reducing the space-heating buffer volume increases the objective by approximately 151 %, while increasing it has little effect;
* increasing the PV scale beyond the optimisation bound reduces the objective by approximately 3.8 %;
* changing the battery capacity by 10 % changes the objective by less than 0.2 % in either direction.

<div style="width: 100%; height: 550px; overflow: hidden; margin-bottom: -1rem;">
    <iframe
        src="../fig/examples/260731_parameter_study_plots_local_sensitivity_response_overview.html"
        title="Local-sensitivity overview of the multi-family house parameter study"
        loading="lazy"
        style="
            width: calc(100% / 0.9);
            height: calc(550px / 0.9);
            border: 0;
            transform: scale(0.9);
            transform-origin: top left;
        "
    ></iframe>
</div>

[Open the local-sensitivity response overview in a separate page](fig/examples/260731_parameter_study_plots_local_sensitivity_response_overview.html)

Reducing the heat-pump power or buffer volume causes a sharp increase in the objective, indicating that both are close to a sizing boundary. Additional PV  above the upper bound of the optimisation improves the result, suggesting that its upper bound should be extended, while moderate changes in battery capacity have little effect.

The response of each parameter can be examined in more detail in the [local-sensitivity trends plot](fig/examples/260731_parameter_study_plots_local_sensitivity_response_trends.html).

