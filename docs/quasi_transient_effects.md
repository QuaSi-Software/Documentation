# General transient effects

## Reduction of usable heat during start-up of each component
The reduction of the usable heat output during start-up of a system can be described using either linear oder exponential start-up and cool-down ramps. Both are described in the following.

### Linear start-up
The following figure illustrate a linear start-up and cool-down behaviour characerized by the start-up time (SUT) and cool-down time (CDT) the system needs to reach full thermal energy output or to cool down completely.

![Heat reduction during start-up](fig/221028_Start-up-Reduction_general.svg)

The current thermal power output can be expressed with the following sectionally defined function. The simulation engine tracks the time an energy system is running or not running. The on-time \(t_{on}\) represents the time since the last start-up of the energy system while \(t_{off}\) is the time since the last shut-down. To handle the case when the energy system has not cooled down completely since the last shut-down, the linear start-up curve can be shifted using \(t_{shift}\) to represent a warm start:

$$
 \dot{Q}_{out,current}(t_{on})  = \dot{Q}_{stationary} 
\begin{cases}
 \frac{t_{on}+t_{shift}}{\text{SUT}} & \text{ for } t_{on}+t_{shift} \ < \text{SUT} \\
1 & \text{ for } t_{on}+t_{shift} \ \geq  \text{SUT}
\end{cases} 
$$

The required timeshift \(t_{shift}\) of the warming-up curve can be calculated within the timestep where the energy system is turned on again using the cooling-down curve and the time since the last shut-down:

$$
\dot{Q}_{out,current}(t_{off}) = \text{max} \left ( \dot{Q}_{out,current}(t_{on}) \left ( 1-\frac{t_{off}}{\text{CDT}} \right ),0 \right ) 
$$
that leads with \(\dot{Q}_{out,current}(t_{on}=0) = \dot{Q}_{out,current}(t_{off})\) to 
$$
t_{shift} = \text{max} \left ( \frac{\dot{Q}_{out,current}(t_{on})}{\dot{Q}_{stationary} } \left( \text{SUT} - t_{off} \frac{\text{SUT}}{\text{CDT}} \right ), 0 \right )
$$

With this information, the average thermal power output in the current timestep between \(t_{on,lower}\) and \(t_{on,upper}\) can be calculated using the integral of the sectionally defined function above:

$$
 \dot{Q}_{out} = \frac{\dot{Q}_{stationary}}{t_{on,upper}-t_{on,lower}}
\begin{cases}
 \frac{t_{shift} \ (t_{on,upper}-t_{on,lower}) + \frac{1}{2} \ (t_{on,upper}^2-t_{on,lower}^2)}{\text{SUT}} & \text{ for } t_{on}+t_{shift} \ < \text{SUT} \\
t_{on,upper}-t_{on,lower} & \text{ for } t_{on}+t_{shift} \ \geq  \text{SUT}
\end{cases} 
$$

This time-averaged integral results in the following yellow curve that represents the normalized average thermal power output, calculated in each timestep with the lower time bound of \(t_{on,lower} = 0\):

![transient shut-down and turn-on effects linear](fig/220223_transient_on_off_linear.JPG)

Note that \(t_{shift}\) has to be set to zero at the first timestep of the simulation and \(t_{on,lower}\) and \(t_{on,upper}\) have to start couting again at every change of operation (on/off, not part-load).

### Exponential start-up
While the method above describes a linear thermal power output during the heat-up of an energy system that requires the integration of sectionally defined functions, the calculation of the time-step averaged thermal power can be also performed using continious exponential functions. This is described for excample in the TRNSYSType 401[^Wetter1996]. The time span for each energy system to heat up is defined by the constant heat-up-time \(\tau_{on}\) and the cool-down time \(\tau_{off}\). This is not the same time span as defined above (SUT and CDT) for the linear warm-up! The following figure shows an exemplary operation curve, analogous to the one for linear transient effects above. An energy system is started from a cool basis, heated up to nominal thermal power output, then shut down and restarted before the system has cooled down completely.

![transient shut-down and tun-on effects exponential](fig/220223_transient_on_off.JPG)

The calculation of the reduced heat output due to transient effects at current time \(t_{on}\) since the last start of the energy system and with the constant heat-up-time \(\tau_{on}\) of each energy system can be calculated with the following expression:
$$
\dot{Q}_{out,current}(t_{on}) = \dot{Q}_{stationary} \left (1 - e^{-\frac{t_{on}}{\tau_{on}}} \right )
$$

If the system has not been cooled town completely since the last shut-down, the heat-up losses can be calculated using the following equation with \(t_{shift}\) representing the time shift for the exponential function (compare to figure above).
$$
\dot{Q}_{out,current}(t_{on}) = \dot{Q}_{stationary} \left (1 - e^{-\frac{t_{shift} + t_{on}}{\tau_{on}}} \right )
\ \ \text{  with  } \ \ t_{shift} = - \tau_{on} \ ln \left ( 1-\frac{\dot{Q}_{out,current}(t_{off})}{\dot{Q}_{stationary}} \right )
$$

The cool-down curve is calculated analogously in order to get the current state of the system in the case of restart in the next time step.
$$
\dot{Q}_{out,current}(t_{off}) = \dot{Q}_{stationary} \left (e^{-\frac{t_{shift}+t_{off}}{\tau_{off}}} \right ) \ \ \text{  with  } \ \ t_{shift} = - \tau_{off} \ ln \left ( 1-\frac{\dot{Q}_{out,current}(t_{on})}{\dot{Q}_{stationary}} \right )
$$

To get the average thermal energy output within the current timestep between \(t_{on,lower}\) and \(t_{on,upper}\), an integration of the exponential function is needed. According to the TRNSYS Type 401[^Wetter1996], this leads to

$$
\dot{Q}_{out} = \dot{Q}_{stationary} \left ( 1 + \frac{\tau_{on}}{t_{on,upper}-t_{on,lower}} \ e^{-\frac{t_{shift}}{\tau_{on}}} \ \left ( e^{-\frac{t_{on,upper}}{\tau_{on}}} - e^{-\frac{t_{on,lower}}{\tau_{on}}} \right )   \right )
$$

[^Wetter1996]: Wetter M., Afjei T.: TRNSYS Type 401 - Kompressionswärmepumpe inklusive Frost- und Taktverluste. Modellbeschreibung und Implementation in TRNSYS (1996). Zentralschweizerisches Technikum Luzern, Ingenieurschule HTL. URL: [https://trnsys.de/static/05dea6f31c3fc32b8db8db01927509ce/ts_type_401_de.pdf](https://trnsys.de/static/05dea6f31c3fc32b8db8db01927509ce/ts_type_401_de.pdf)

## Non-linear part-load efficiency

Most of the energy systems can be operated not only at full load, but also in part load operation. Due to several effects like the efficiency of electrical motors, inverters or thermal capacity effects, the efficiency of an energy system in part load usually differs from its efficiency at its full load operation point. How exactly the efficiency changes in part load depends on the specific energy system. Here, the general approach implemented in the simulation model is explained to consider part-load dependent efficencies. This method needs to be extended for heat pumps which is described in the corresponding section.

The part-load ratio (PLR) in general is defined as:

\(PLR = \frac{\text{average loading power (el. or th.) of energy system during current time step}}{\text{maximal possible power (el. or th.) of energy system}} \)

The change of the efficiency with respect to the PLR can be given as curve, for example as shown in the following figure for the efficiency of a motor in part-load operation (Source: Eppinger2021[^Eppinger2021]):

<img src="/fig/230124_motor_efficiency_Eppinger2021.JPG" alt="test" width="500"/>

Considering non-linear part-load efficiencies leads to several problems. First, the part-load efficiency curve is not necessarily a monotonic function, as shown in the figure above exemplarily. This implies that the function is also non-invertible. However, the inversion is needed to determine the part-load state at which a power system has so be operated at the current time step when external limits are present, e.g. if only a limited energy supply and/or a limited energy demand is given. 

Another problem is the fact, that efficiencies are always defined as ratios. When changing the efficiency due to part-load operation, it is not clear, how the two elements of the efficiency-ratio have to be adjusted as only their ratio is given. Here, in this simulation model, one input or one output has to be defined as basis for the PLR that will be considered to have a linear behaviour in part-load operation. The other in- or output energies will be adjusted to represent the non-linearities in the change of the efficiency. 

A third difficulty is the inconsistent definition of the part-load ratio in the literature when considering non-linearities in part-load operation. In theory, every input and output has its own part-load ratio at a certain operation point. Each of the PLR do not necessarily represent the same operational state of the energy system, so this would lead to an inconsistent base if several operational restrictions are given. Using the assumption above helps to handle this issue - the reference part-load ratio is user-defined for each energy system and this is assumed to have a linear relation to the part-load.

In the figure below, a part-load curve (orange curve) based on an exponential function of a fictitious energy system that has electricity as input (yellow curve) and heat as output (grey curve) is shown. The heat output is assumed to be linear (straight line) with a rated power of 1 kW, resulting in a non-linear demand of electricity. 
![general non-linear part-load of energy systems](fig/230125_non-linear_PLR_general.JPG)

The basis for the consideration of non-linear part-load efficiencies is the efficiency curve of an energy system

\(\eta(PLR)=f(PLR)\)

as shown exemplarily as orange curve in the figure above. \(f(PLR)\) can be a linear, an exponential or a partially defined function. It can also be a non-monotonic function as long as the function of the electrical input power (yellow curve)

\(P(PLR)=\eta(PLR) \ \ PLR \ \ P_{rated}\) 

is monotonic in the range of \(PLR=0:1\). This is the case for all common part-load functions as the change in efficiency is not as big as the impact of the PLR on \(P(PLR)\). During preprocessing, the function \(P(PLR)\) is calculated from \(\eta(PLR)\) and inverted to get \(PLR(P)\). The part-load function of the heat output, that is assumed to be linear,

\(Q(PLR) = PLR \ \ Q_{rated}\)

needs to be inverted as well. As \(Q(PLR)\) is linear, the inverse is trivial and meets the original definition of the PLR:

\(PLR(Q_{demand}) = \frac{Q_{demand}}{Q_{rated}}\).

During each timestep, both functions are evaluated according to the operational strategy to determine the part load ratio that is needed to meet the demand while not exeeding the maximum abailable power.

If several outputs on an energy system exist, like with an combined heat and power plant, each output can have its own independent efficiency curve, but the part-load factor should then be based on the same definition to provide a consistent base.


- Bezugsgröße für Berechnung der PLR
- Aufteilung der Wirkungsgradänderung auf Input/Output

In order to be able to consider the part load dependency of the thermal and electrical efficiency (\(\eta_{thermal}\) and \(\eta_{el}\)) during the simulation in a computaninally efficient way, they can be given as independent curves with respect to the part load ratio (PLR) as \(\eta_{CHP}(PLR)=f(PLR)\). During the preprocessing, both efficiency curves are used to calculate the part-load dependend power curves for the electical and thermal power as \(P(PLR)=\eta_{CHP}(PLR) \ \ PLR \ \ P_{rated}\). This works also for non-monotonic efficiency functions as long as \(P(PLR)\) is monotonic in the range of \(PLR=0:1\). During preprocessing, each function \(P(PLR)\) is inverted to get \(PLR(P)\). During each timestep, this function is evaluated according to the operational strategy to determine the part load ratio.

[^Eppinger2021]: Eppinger, B. et al.(2021): Simulation of the Part Load Behavior of Combined Heat Pump-Organic Rankine Cycle Systems. In: *Energies 14 (13)*, S. 3870. doi: [10.3390/en14133870](https://doi.org/10.3390/en14133870).