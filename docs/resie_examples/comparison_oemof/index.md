# Comparing a complex energy system between ReSiE and oemof

![Energy flow of electrolyser](energy_system.svg)

## Description of energy system
* Technologies (heat pump, hydrogen electrolyser, etc.)
* Operational strategies used (priorities, hysteresis, HEL power limitations)
* Main heat bus to two smaller busses: reason as prioritiy to one, peak load only in other bus

## Differences between models
* ReSiE modelled as described (because it is the base)
* oemof does not implement operational strategies the same way
* priorities as costs??? In comparision to ReSiE the simulation framework oemof uses another form of energy prioritization, naimly cost prioritization.
* hysteresis not used at all???
* HEL power limitation???
* disabled connections (battery, HP of STES)
* minimum run time
* minimum partial load

## Simulation results
* chart with monthly energy balances (ReSiE & oemof)
* chart for electricity (and H2) over the year (ReSiE & oemof)
* chart for heat over the year (ReSiE & oemof)
* chart with details over a few days with interesting results about STES and STTES (ReSiE, maybe oemof)
* discussion of differences:
    * possible causes for differences
    * which modelling differences show in the results and which don't
