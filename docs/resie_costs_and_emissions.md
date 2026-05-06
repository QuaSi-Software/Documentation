# Technical description of Costs and Emissions

## Costs

The economic evaluation calculates annualized economic values for an energy system simulation from component-specific investment data, operation-related costs, and simulated energy flows. The calculation follows an annuity-based approach according to VDI 2067[^VDI2067].

[^VDI2067]: Verein Deutscher Ingenieure e.V.: VDI 2067 Blatt 1 / Part 1 - Wirtschaftlichkeit gebäudetechnischer Anlagen. Grundlagen und Kostenberechnung / Economic efficiency of building installations. Fundamentals and economic calculation (September 2012). Düsseldorf.

The economic result is calculated over a defined observation period. If the simulated output period is shorter than the economic observation period, the relevant time series are extended by repeating the configured repeat period until the full observation period is covered. Leap days are ignored as in the energy system simulation.

**Costs are reported as positive values and revenues are reported as negative values**. This sign convention differs from the sign convention used in VDI 2067.

The total annuity of the energy system is calculated as

\[
A_\mathrm{tot} =
A_\mathrm{capex}
+
A_\mathrm{opex}
+
A_\mathrm{en}
\]

where \(A_\mathrm{tot}\) is the total annuity, \(A_\mathrm{capex}\) is the annuity of capital-related costs, \(A_\mathrm{opex}\) is the annuity of operation-related costs excluding energy flows, and \(A_\mathrm{en}\) is the annuity of energy-related costs and revenues.

### Energy-related cashflows

Energy-related costs and revenues are calculated from the simulated energy profiles of source and sink components. For source components, the output energy is interpreted as supplied energy and is assigned to energy costs. For sink components, the input energy is interpreted as accepted energy and is assigned to energy revenues.

For each time step, the energy amount is multiplied by an energy price. The price may either be given as a constant value or as a time-dependent price profile. The resulting time-step values are aggregated to yearly cashflows and scaled with an annual price change factor.

For one component, the nominal yearly energy cashflow is calculated as

\[
C_{\mathrm{en},y}
=
s
\left(
\sum_{t \in T_y}
E_t \, p_t
\right)
\cdot
r_\mathrm{en}^{\,y-1}
+
s \,
C_\mathrm{base}
\cdot
r_\mathrm{base}^{\,y-1}
\]

where \(C_{\mathrm{en},y}\) is the nominal energy-related cashflow in year \(y\), \(E_t\) is the energy amount in time step \(t\), \(p_t\) is the energy price in time step \(t\), \(T_y\) is the set of time steps assigned to year \(y\), \(C_\mathrm{base}\) is the yearly base cost, \(r_\mathrm{en}\) is the annual energy price change factor, \(r_\mathrm{base}\) is the annual base cost change factor, and \(s\) is the sign factor.

The sign factor is defined as

\[
s =
\begin{cases}
+1, & \text{for source components} \\
-1, & \text{for sink components}
\end{cases}
\]

Thus, energy flows from source components lead to positive costs, while energy flows into sink components lead to negative revenues.

### Unmet energy

For fixed source and fixed sink components, unmet energy is evaluated separately. The unmet energy is calculated from the difference between the specified supply or demand and the actual simulated energy flow.

For fixed source components, the unmet supply is calculated as

\[
E_{\mathrm{unmet},t}
=
E_{\mathrm{supply},t}
-
E_{\mathrm{out},t}
\]

For fixed sink components, the unmet demand is calculated as

\[
E_{\mathrm{unmet},t}
=
E_{\mathrm{demand},t}
-
E_{\mathrm{in},t}
\]

where \(E_{\mathrm{unmet},t}\) is the unmet energy in time step \(t\), \(E_{\mathrm{supply},t}\) is the requested source supply, \(E_{\mathrm{out},t}\) is the actual source output, \(E_{\mathrm{demand},t}\) is the requested sink demand, and \(E_{\mathrm{in},t}\) is the actual sink input.

**Unmet energies of both sinks and sources are treated as positive penalty costs**. The nominal yearly cashflow of unmet energy is calculated as

\[
C_{\mathrm{unmet},y}
=
\left(
\sum_{t \in T_y}
E_{\mathrm{unmet},t} \, p_{\mathrm{unmet},t}
\right)
\cdot
r_\mathrm{unmet}^{\,y-1}
\]

where \(p_{\mathrm{unmet},t}\) is the price of unmet energy in time step \(t\) and \(r_\mathrm{unmet}\) is the annual price change factor of unmet energy.

### Capital-related cashflows

Capital-related cashflows include the initial investment, replacement investments, residual values, and subsidies. The initial investment is calculated from a component-specific capital expenditure function and a component-specific reference quantity, for example installed power, storage capacity, or area.

The initial investment \(I_0\) is calculated as

\[
I_0 = f_\mathrm{capex}(x_\mathrm{ref})
\]

where \(f_\mathrm{capex}\) is the component-specific investment cost function, and \(x_\mathrm{ref}\) is the component-specific reference quantity.

Replacement investments are included if the component lifetime is shorter than the observation period. The replacement investment  \(I_j\) at replacement time \(t_j\) is calculated as

\[
I_j =
I_0 \,
r_\mathrm{capex}^{\,t_j}
\]

where \(r_\mathrm{capex}\) is the annual price change factor of capital expenditure, and \(t_j\) is the replacement time in years after the beginning of the observation period. For non-integer component lifetimes, replacement times are mapped to yearly cashflow buckets by rounding the replacement time \(t_j\) to the nearest integer year. The replacement investment amount is escalated using the exact value of \(t_j\), but discounting is based on the rounded yearly cashflow bucket. Replacements whose rounded year index lies outside the observation period are not included.

A residual value \(R_N\) is considered at the end of the observation period if the last investment still has a remaining technical lifetime. The residual value is calculated proportionally to the unused lifetime share:

\[
R_N =
I_\mathrm{last}
\frac{L_\mathrm{rem}}{L}
\]

where \(I_\mathrm{last}\) is the value of the last investment, \(L_\mathrm{rem}\) is the remaining lifetime after the observation period, and \(L\) is the technical lifetime.

Subsidies are considered as one-time revenues at the beginning of the observation period. If a maximum subsidy is defined, the subsidy is limited by this maximum value:

\[
S_0 =
\min
\left(
I_0 \, f_\mathrm{sub},
S_\mathrm{max}
\right)
\]

where \(S_0\) is the subsidy, \(f_\mathrm{sub}\) is the subsidy rate of the capital expenditure, and \(S_\mathrm{max}\) is the maximum subsidy.

The capital-related annuity is calculated from the discounted investments, subsidies, and residual values.

### Operation-related cashflows

Operation-related cashflows include maintenance and inspection costs, repair costs, labour costs, and optional component-specific additional operating costs. Energy-related costs are not included in this category because they are calculated separately from the simulated energy flows.

Maintenance and inspection costs \(C_{\mathrm{maint},y}\) in year \(y\) are calculated as a yearly fraction of the initial investment \(I_0\):

\[
C_{\mathrm{maint},y}
=
I_0 \,
f_\mathrm{maint}
\,
r_\mathrm{maint}^{\,y-1}
\]

Repair costs \(C_{\mathrm{repair},y}\) in year \(y\) are calculated analogously:

\[
C_{\mathrm{repair},y}
=
I_0 \,
f_\mathrm{repair}
\,
r_\mathrm{repair}^{\,y-1}
\]

Labour costs  \(C_{\mathrm{labour},y}\) in year \(y\) are calculated from the yearly labour demand \(h_\mathrm{labour}\) and the labour cost rate  \(c_\mathrm{labour}\):

\[
C_{\mathrm{labour},y}
=
h_\mathrm{labour}
\,
c_\mathrm{labour}
\,
r_\mathrm{labour}^{\,y-1}
\]

where  \(f_\mathrm{maint}\) is the maintenance and inspection rate, \(f_\mathrm{repair}\) is the repair rate, and \(r_\mathrm{maint}\), \(r_\mathrm{repair}\), and \(r_\mathrm{labour}\) are the corresponding annual price change factors.

Additional component-specific operating costs may be added where required. These may represent material flows or other costs that are not represented by the energy interfaces of the component.

### Discounting and annuity calculation

All yearly cashflows are discounted to present values before they are converted to an annuity. 

The timing of the cashflows is defined by the economic event represented by each cost or revenue is chosen according to VDI 2067. Cashflows that are assumed to occur at the beginning of a year are discounted with the time index \(y-1\). Cashflows that are assumed to occur at the end of a year are discounted with the time index \(y\).

The following timing convention is used:

| Cashflow | Timing | Description |
|---|---|---|
| initial investment | beginning of year 1 | investment at the start of the observation period |
| replacement investment | beginning of the replacement year | reinvestment when the component lifetime is reached |
| subsidy | beginning of year 1 | one-time subsidy related to the initial investment |
| residual value | end of final year | remaining component value at the end of the observation period |
| energy costs and revenues | end of each year | yearly costs or revenues resulting from simulated energy flows |
| unmet energy costs | end of each year | yearly penalty costs for unmet demand or supply |
| base costs and revenues | end of each year | fixed yearly costs or revenues assigned to an energy flow component |
| maintenance and inspection costs | end of each year | yearly operation-related costs based on the initial investment |
| repair costs | end of each year | yearly repair costs based on the initial investment |
| labour costs | end of each year | yearly operational labour costs |
| additional component-specific opex | end of each year | additional yearly operating costs or revenues not represented by energy interfaces |

For an observation period of \(N\) years, the first year has the index \(y = 1\). A cashflow at the beginning of year \(y\) is therefore assigned to the time \(y-1\), while a cashflow at the end of year \(y\) is assigned to the time \(y\).

The discount factor is calculated from the interest rate:

\[
q = 1 + i
\]

where \(q\) is the discount factor and \(i\) is the interest rate.

Cashflows occurring at the end of a year are discounted as

\[
C_{0,y} = \frac{C_y}{q^y}
\]

Cashflows occurring at the beginning of a year are discounted as

\[
C_{0,y} = \frac{C_y}{q^{y-1}}
\]

where \(C_y\) is the nominal cashflow in year \(y\) and \(C_{0,y}\) is the corresponding present value.

The annuity factor for an observation period of \(N\) years is calculated as

\[
a_N = \frac{q^N (q - 1)} {q^N - 1}
\]

For an interest rate close to zero, the annuity factor is simplified to

\[
a_N = \frac{1}{N}
\]

The annuity \(A\)  of a cashflow series is calculated from the sum of the discounted yearly values:

\[
A = a_N \sum_{y=1}^{N} C_{0,y}
\]

where \(a_N\) is the annuity factor, \(N\) is the observation period in years, and \(C_{0,y}\) is the discounted cashflow in year \(y\).

### Economic result

The economic result contains the total annuity and the annuity contributions of the main cost categories:

\[
A_\mathrm{tot}
=
A_\mathrm{capex}
+
A_\mathrm{opex}
+
A_\mathrm{en}
\]

The following economic KPIs are reported:

| Symbol | Description | Unit |
|---|---|---|
| \(A_\mathrm{tot}\) | total annuity of the energy system | [€/a] |
| \(A_\mathrm{capex}\) | annuity of capital-related costs | [€/a] |
| \(A_\mathrm{opex}\) | annuity of operation-related costs without energy costs | [€/a] |
| \(A_\mathrm{en}\) | annuity of energy-related costs, revenues, and unmet energy penalties | [€/a] |

The result also contains a component-wise breakdown. For each component, the yearly nominal cashflows, discounted present values, and resulting annuities are stored where applicable. This breakdown is used for exporting tabular economic results and for plotting yearly or discounted economic cashflows.

### Notes / Conventions

Costs are positive and revenues are negative in all exported economic results.

Unmet energies of both sinks and sources are treated as positive penalty costs

If the simulation period is shorter than the economic observation period, the profiles are extended by repetition. The economic result therefore depends on the selected repeat period.

The current implementation does not include possible effects of storage state differences between the beginning and end of the economic observation period.

## Greenhouse Gas Emissions

The emissions evaluation calculates GHG emissions and emission credits for an energy system simulation based on simulated energy flows and component-specific embodied emissions.

The result is calculated over a defined emissions observation period. If the simulated output period is shorter than the emissions observation period, the relevant time series are extended by repeating the configured repeat period until the full observation period is covered. Leap days are ignored.

**GHG emissions released to the environment are reported as positive values. Credits or avoided emissions are reported as negative values.**

Emission credits should be assigned with care. In general, emission credits represent avoided emissions outside the considered energy system boundary. They may be used, for example, if an energy flow into a sink component is interpreted as a useful output that replaces an external reference process. Assigning such credits is optional and depends on the intended balance boundary. If credits are assigned, it has to be checked whether the credited avoided emissions are already considered elsewhere in the model or in another downstream process.

The emissions assigned to energy flows depend on the emission factors provided by the user. Therefore, the interpretation of the resulting emission balance also depends on the scope represented by these factors. For example, an emission factor may represent only direct emissions during energy conversion, upstream emissions from fuel or energy provision, or a broader life-cycle emission factor. 
The model does not distinguish these scopes internally. It multiplies the simulated energy flows with the provided emission factors and aggregates the resulting emissions or credits. Users are therefore responsible for selecting emission factors that are consistent with the intended balance boundary and for documenting whether the reported results represent direct emissions, upstream emissions, life-cycle emissions, or another defined scope.

The total emissions \(G_\mathrm{tot}\) of the energy system are calculated as

$$
G_\mathrm{tot}
=
G_\mathrm{en}
+
G_\mathrm{emb}
$$

where \(G_\mathrm{en}\) are the emissions from energy flows, and \(G_\mathrm{emb}\) are the embodied emissions.

### Energy-related emissions

Energy-related GHG emissions and emission credits are calculated from the simulated energy profiles of source and sink components. For source components, the output energy is interpreted as supplied energy and is assigned to emissions. For sink components, the input energy is interpreted as accepted energy and is assigned to emission credits.

For each time step, the energy amount is multiplied by an emission factor. The emission factor may either be given as a constant value or as a time-dependent emission profile. The resulting time-step values are aggregated to yearly emissions and scaled with an annual emission factor change rate.

For one component, the nominal yearly energy-related emissions  \(G_{\mathrm{en},y}\) in year \(y\) are calculated as

$$
G_{\mathrm{en},y}
=
s
\left(
\sum_{t \in T_y}
E_t \, g_t
\right)
\cdot
r_\mathrm{en}^{\,y-1}
$$

where \(E_t\) is the energy amount in time step \(t\), \(g_t\) is the emission factor in time step \(t\), \(T_y\) is the set of time steps assigned to year \(y\), \(r_\mathrm{en}\) is the annual change factor of the energy emission factor, and \(s\) is the sign factor.

The annual change factor is calculated as

$$
r_\mathrm{en}
=
1
+
\Delta g_\mathrm{en}
$$

where \(\Delta g_\mathrm{en}\) is the annual change rate of the energy emission factor.

The sign factor is defined as

$$
s =
\begin{cases}
+1, & \text{for source components} \\
-1, & \text{for sink components}
\end{cases}
$$

Thus, energy flows from source components lead to positive emissions, while energy flows into sink components lead to negative emission credits.

The total energy-related emissions are calculated by summing all yearly energy-related emissions over all relevant components:

$$
G_\mathrm{en}
=
\sum_c
\sum_{y=1}^{N}
G_{\mathrm{en},c,y}
$$

where \(G_{\mathrm{en},c,y}\) are the energy-related emissions of component \(c\) in year \(y\), and \(N\) is the emissions observation period in years.

### Embodied emissions

Embodied emissions describe emissions associated with the provision of a component, for example from manufacturing, transport, installation, and end-of-life processes if these are included in the configured embodied emission factor. Embodied emissions are calculated for all non-bus components if embodied emissions are enabled in the emissions parameters.

The initial embodied emissions \(G_0\) are calculated from a component-specific embodied emission function and a component-specific reference quantity, for example installed power, storage capacity, or area:

$$
G_0
=
f_\mathrm{emb}(x_\mathrm{ref})
$$

where \(f_\mathrm{emb}\) is the component-specific embodied emission function, and \(x_\mathrm{ref}\) is the component-specific reference quantity.

Replacement emissions are included if the component lifetime is shorter than the emissions observation period. The embodied emissions of a replacement  \(G_j\)  at replacement time \(t_j\) are calculated as

$$
G_j
=
G_0
\,
r_\mathrm{emb}^{\,t_j}
$$

where \(r_\mathrm{emb}\) is the annual change factor of embodied emissions, and \(t_j\) is the replacement time in years after the beginning of the observation period.

For non-integer component lifetimes, replacement times are mapped to yearly emission buckets by rounding the replacement time \(t_j\) to the nearest integer year. The replacement emission amount is scaled using the exact value of \(t_j\), but the yearly assignment is based on the rounded year index used internally. Replacements whose rounded year index lies outside the observation period are not included.

The annual change factor of embodied emissions is calculated as

$$
r_\mathrm{emb}
=
1
+
\Delta g_\mathrm{emb}
$$

where \(\Delta g_\mathrm{emb}\) is the annual change rate of embodied emissions.

A residual emission credit is considered at the end of the observation period if the last installed component still has a remaining technical lifetime. The residual credit \(G_{\mathrm{res},N}\) in the final year \(N\) is calculated proportionally to the unused lifetime share:

$$
G_{\mathrm{res},N}
=
-
G_\mathrm{last}
\frac{L_\mathrm{rem}}{L}
$$

where \(G_\mathrm{last}\) are the embodied emissions of the last installation or replacement, \(L_\mathrm{rem}\) is the remaining lifetime after the observation period, and \(L\) is the technical lifetime.

The total embodied emissions \(G_{\mathrm{emb},c}\) of component \(c\) are calculated as

$$
G_{\mathrm{emb},c}
=
G_0
+
\sum_{j=1}^{n}
G_j
+
G_{\mathrm{res},N}
$$

where \(n\) is the number of replacements within the observation period.

The total embodied emissions of the energy system are calculated as

$$
G_\mathrm{emb}
=
\sum_c
G_{\mathrm{emb},c}
$$

### Emissions result

The emissions result contains the total emissions and the contributions of the main emissions categories:

$$
G_\mathrm{tot}
=
G_\mathrm{en}
+
G_\mathrm{emb}
$$

The following emissions KPIs are reported:

| Symbol | Description | Unit |
|---|---|---|
| \(G_\mathrm{tot}\) | total emissions of the energy system | [kgCO₂e] |
| \(G_\mathrm{en}\) | emissions and credits from energy flows | [kgCO₂e] |
| \(G_\mathrm{emb}\) | embodied emissions including replacements and residual credits | [kgCO₂e] |

The result also contains a component-wise breakdown. For each component, the yearly emission series and aggregated emission values are stored where applicable. This breakdown is used for exporting tabular emissions results and for plotting yearly and cumulative emissions.

### Notes / Conventions

Positive values represent emissions to the environment. Negative values represent credits or avoided emissions.

Energy emission factors may be constant or time-dependent. Time-dependent emission profiles are extended to the full emissions observation period in the same way as the corresponding energy profiles.

No explicit end-of-life emissions are calculated separately. If end-of-life emissions shall be considered, they have to be included in the configured embodied emissions.

Internally, emissions are calculated in grams of CO₂-equivalent. For plots and CSV exports, the values are converted to kilograms of CO₂-equivalent.