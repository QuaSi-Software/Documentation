# Technical description of Optimisation and Sensitivity analysis

## Optimisation

Optimisation varies selected input parameters within defined ranges and repeatedly evaluates the complete energy-system simulation. Each simulation run represents one candidate system design. Its result is reduced to one or more objective values, which the selected optimisation algorithm uses to decide which parameter combinations should be evaluated next.

Typical optimisation parameters are component sizes, capacities, or other numerical inputs that influence system design or operation. Each parameter is varied within a defined physical range.

The configuration syntax, available objective definitions, parameter fields, optimisation settings, and output settings are described in the [input file format](resie_input_file_format.md#parameter-study-optimisation).

### Objective values

The objective defines what the optimisation should improve. It is calculated from the result of each complete simulation run. Depending on the project configuration, the objective may represent one quantity, such as annual costs, or several quantities, such as costs and emissions.

In a single-objective optimisation, every simulation run with a given parameter combination results to one scalar objective value. The optimisation searches for the parameter combination with the lowest objective value. Objectives that should be maximised must therefore be converted into an equivalent minimisation objective by applying the configured sign convention.

Several result quantities can also be combined into one scalar objective. A sum treats all included quantities equally after any configured scaling. A linear combination assigns an individual weight to every quantity. The weights should reflect both the intended priorities and the numerical magnitude of the quantities. Otherwise, an objective with large numerical values may dominate the result even when it is not intended to be more important.

In a multi-objective optimisation, all configured objective values are retained separately. There is generally no single best solution when objectives conflict. Instead, the result is a set of non-dominated solutions. A solution is non-dominated when no other evaluated solution improves one objective without worsening at least one other objective. This set represents the available trade-offs, for example between annual costs and emissions.

### Optimisation process

The optimisation process follows these steps:

1. The selected parameter values are inserted into a copy of the project configuration.
2. The complete energy-system simulation is run with this modified configuration.
3. The configured objective value or objective vector is calculated from the simulation result.
4. The result, including the physical parameter values, is stored.
5. The optimisation algorithm selects further parameter combinations based on the results obtained so far.

Every objective evaluation is therefore a complete simulation. The required runtime depends mainly on the number of evaluations and the runtime of an individual simulation. Global and population-based algorithms usually require more evaluations than local algorithms, but are less dependent on a suitable starting point.

For single-objective studies, the best successfully evaluated result is reported after the optimisation. For multi-objective studies, no single result is reported as best because the preferred compromise depends on the user's priorities.

### Interpreting optimisation results

For a single-objective study, the reported best result is the successfully evaluated parameter combination with the lowest objective value. It is the best result found within the evaluated runs, not a mathematical proof that no better solution exists. The confidence in the result depends on the selected algorithm, bounds, starting point, and evaluation budget.

A lower objective value means a better result only according to the configured objective. The selected design should also be checked using its complete simulation outputs. Aggregated objectives can hide undesirable behavior, such as unmet demand, excessive cycling, or a poor result in a quantity that received little weight.

A best parameter value at or very close to a lower or upper bound indicates that the bound is active. This may be a valid design conclusion, but it can also mean that a better solution lies outside the investigated range. In that case, the technical validity of extending the range should be assessed before repeating the optimisation.

For stochastic global algorithms, repeated runs may produce different best results. Similar objective values from several runs increase confidence that the relevant region has been found. A subsequent local refinement can improve numerical precision around the best global result, but it does not compensate for an unsuitable search range or objective definition.

For a multi-objective study, the result is a non-dominated set rather than one best design. The trade-off should be inspected across all objectives. A practical choice is often located near a bend in the trade-off front, where a small improvement in one objective would require a large deterioration in another. The final selection still depends on priorities that are not contained in the optimisation itself.

### Starting points, bounds, and refinement

Local optimisation algorithms require a starting point. This point should represent a valid and plausible system design and must lie within the configured parameter bounds. A good starting point can reduce the number of evaluations and can influence which local optimum is found.

Global algorithms explore the complete bounded parameter space and are therefore less dependent on the start values. However, the selected bounds remain important. Very wide bounds increase the search space and may require substantially more evaluations. Bounds should therefore cover all technically and economically relevant values without including implausible regions.

A completed single-objective optimisation can optionally be followed by a refinement stage. The best parameter combination found by the first stage is used as the starting point for a second optimiser. A common approach is to perform a broad global search first and then refine the best result with a local algorithm. Refinement is not applied to multi-objective optimisation because a multi-objective result does not provide one unique best starting point.

### Parallel execution and interruption

Algorithms that evaluate populations of candidate solutions can distribute simulation runs over several Julia threads. Parallel execution is most effective when individual simulations are expensive and enough candidates can be evaluated simultaneously. Algorithms that choose each new point from the immediately preceding result remain serial.

The study can be interrupted with `Ctrl+C`. Completed simulation runs are retained, and the best available single-objective result is reported from the runs completed before the interruption.

### Choosing an optimisation algorithm

The following tables provide a selection of suitable algorithms for common optimisation problems in ReSiE. Below is a brief guide to help you select an appropriate algorithm based on the system you want to simulate. If you don't want to think about it, use `NLopt: LN_NELDERMEAD` for a local single objective optimisation if you know good start values and  `Metaheuristics: NSGA3` for multi objective problems.

**Single objective**

| Situation                                                                       | Type and algorithm                                    |
| ------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Local search with an approximately smooth objective                             | `NLopt: LN_BOBYQA`                                    |
| Local search with a nonsmooth or uncertain objective                            | `NLopt: LN_SBPLX`  OR  `NLopt: LN_NELDERMEAD`  (faster, but less explorative)  |
| Global, parallel search with expensive evaluations                              | `Metaheuristics: ECA`                                 |
| Global, parallel search with strong multimodality                               | `Metaheuristics: DE`                                  |
| Global, parallel search with adaptive search parameters                         | `Metaheuristics: SHADE`                               |
| Global, serial and deterministic search with few or moderately separated minima | `NLopt: GN_DIRECT_L`                                  |
| Global, serial and deterministic search with many separated minima              | `NLopt: GN_DIRECT`                                    |
| Global, serial and stochastic search                                            | `BlackBoxOptim: adaptive_de_rand_1_bin_radiuslimited` |

**Multiple objectives**

| Situation                                       | Type and algorithm                                                                |
| ----------------------------------------------- | --------------------------------------------------------------------------------- |
| Only one compromise solution is required        | Combine the objectives into a scalar objective and use the single-objective guide |
| Two or three objectives                         | `Metaheuristics: NSGA2`                                                           |
| More than three objectives                      | `Metaheuristics: NSGA3`                                                           |
| Two objectives with hypervolume-based selection | `Metaheuristics: SMS_EMOA`                                                        |

You can also check the documentation of the supported optimisation packages (`type`) for other optimisation algorithms and use them in ReSiE. Supported packages are `Optim`[^Optim], `BlackBoxOptim`[^BlackBoxOptim], `Metaheuristics`[^Metaheuristics], `NLopt`[^NLopt] and `NOMAD`[^NOMAD].  You then may need to add special options to the algorithm that can be passed using a dictionary for the parameter `optim_kwargs` in the ReSiE input file. 

[^Optim]: [https://julianlsolvers.github.io/Optim.jl/stable/](https://julianlsolvers.github.io/Optim.jl/stable/)
[^BlackBoxOptim]: [https://github.com/SciML/BlackBoxOptim.jl](https://github.com/SciML/BlackBoxOptim.jl)
[^Metaheuristics]: [https://jmejia8.github.io/Metaheuristics.jl/stable/algorithms/](https://jmejia8.github.io/Metaheuristics.jl/stable/algorithms/); Mejía-de-Dios et al., (2022). Metaheuristics: A Julia Package for Single- and Multi-Objective Optimization. Journal of Open Source Software, 7(78), 4723, [https://doi.org/10.21105/joss.04723](https://doi.org/10.21105/joss.04723)
[^NLopt]: [https://nlopt.readthedocs.io/en/latest/NLopt_Algorithms/](https://nlopt.readthedocs.io/en/latest/NLopt_Algorithms/)
[^NOMAD]: [https://bbopt.github.io/NOMAD.jl/stable/](https://bbopt.github.io/NOMAD.jl/stable/)

**Use the following steps to select an algorithm:**

**1. Single or multiple objectives?**

Choose single-objective optimisation when:

* one performance measure dominates the decision;
* several metrics can be combined into one meaningful objective;
* only one final design is required;
* objective priorities or weights are known.

Choose multi-objective optimisation when:

* the objectives conflict;
* no suitable weighting is available;
* trade-offs should remain visible;
* several alternative solutions should be compared.

Typical examples are cost versus emissions or  investment cost versus operating cost.

If only one compromise solution is required, combine the objectives with `sum` or `linear`. Use `multi-objective` when the trade-off itself is part of the result.

**2. Local or global optimisation?**

Choose local optimisation when:

* a good starting point is available;
* only nearby improvement is required;
* separated local optima are unlikely;
* the evaluation budget is small.

Choose global optimisation when:

* the starting point is arbitrary;
* multiple local optima may exist;
* thresholds or operating modes create separated regions;
* broad exploration is required.

**3. Smooth or nonsmooth objective?**

Treat an objective as approximately smooth when small changes in the parameter values produce gradual changes in the objective.

Treat it as nonsmooth or uncertain when the model contains:

* thresholds or on/off logic;
* clipping or saturation;
* piecewise tariffs;
* operating-mode changes;
* large plateaus;
* sudden jumps.

When uncertain, use an algorithm intended for nonsmooth objectives.

**4. Is parallel evaluation available?**

Parallel evaluation means that several parameter combinations are simulated simultaneously. Population-based algorithms such as `ECA`, `DE`, `SHADE`, `NSGA2` and `NSGA3` generally benefit most from parallel execution.

Julia can be started with multiple threads, for example:

```bash
julia --threads 16 --project=. src/resie-cli.jl
```

Choose the number of threads according to the available hardware. Multithreaded optimisation can significantly reduce the runtime when individual simulations are expensive.

## Sensitivity analysis

Sensitivity analysis examines how changes in selected input parameters affect the objective. Unlike optimisation, it does not primarily search for the best design. Its purpose is to identify influential parameters, quantify the response of the objective, and assess how strongly conclusions depend on parameter assumptions.

ReSiE provides two complementary approaches:

* **Local sensitivity analysis** changes one parameter at a time around a defined reference design. It describes the response close to that design.
* **Global sensitivity analysis** varies all selected parameters over their complete configured ranges. It separates individual parameter effects from effects caused by interactions.

Sensitivity analysis can be performed after a parameter variation or optimisation, in which case suitable completed simulations are reused. It can also be run as a standalone study. Reusing results avoids repeating identical simulations.

### Local sensitivity

Local sensitivity analysis evaluates the objective at a reference point and at one lower and one upper value for each selected parameter. Only one parameter is changed at a time; all other parameters remain at their reference values. This method is therefore also called a one-at-a-time analysis.

The reference point can be either:

* the configured parameter start values; or
* the best result of a completed single-objective optimisation.

The second option links the sensitivity analysis directly to the optimised system design. It is not available for multi-objective optimisation because no unique best result exists.

For parameter \(x_i\), the three evaluated values are

\[
x_i^\mathrm{lower}
<
x_i^\mathrm{ref}
<
x_i^\mathrm{upper}
\]

where \(x_i^\mathrm{ref}\) is the reference value. Lower and upper values can be specified explicitly. If they are not specified, they are calculated from the configured relative variation \(v\):

\[
\Delta x_i
=
\left|x_i^\mathrm{ref}\right| v
\]

\[
x_i^\mathrm{lower}
=
x_i^\mathrm{ref}
-
\Delta x_i
\]

\[
x_i^\mathrm{upper}
=
x_i^\mathrm{ref}
+
\Delta x_i
\]

A relative variation cannot be derived when the reference value is zero. In that case, explicit lower and upper values are required.

Local sensitivity points are not limited by the optimisation bounds. This allows the user to define a local interval independently of the range previously used for optimisation. The selected values must nevertheless be physically meaningful and valid for the simulated system.

Let \(f^\mathrm{ref}\) be the objective at the reference point, \(f_i^\mathrm{lower}\) the objective at the lower value, and \(f_i^\mathrm{upper}\) the objective at the upper value. The absolute objective changes are

\[
\Delta f_i^\mathrm{lower}
=
f_i^\mathrm{lower}
-
f^\mathrm{ref}
\]

\[
\Delta f_i^\mathrm{upper}
=
f_i^\mathrm{upper}
-
f^\mathrm{ref}
\]

The corresponding relative changes are calculated as

\[
\Delta f_{i,\mathrm{rel}}^\mathrm{lower}
=
\frac{\Delta f_i^\mathrm{lower}}
{\left|f^\mathrm{ref}\right|}
\]

\[
\Delta f_{i,\mathrm{rel}}^\mathrm{upper}
=
\frac{\Delta f_i^\mathrm{upper}}
{\left|f^\mathrm{ref}\right|}
\]

Relative changes are undefined when the reference objective is zero.

A central finite-difference gradient describes the average objective slope between the lower and upper points:

\[
g_i
=
\frac{
f_i^\mathrm{upper}
-
f_i^\mathrm{lower}
}{
x_i^\mathrm{upper}
-
x_i^\mathrm{lower}
}
\]

The gradient retains the units of the objective divided by the units of the parameter. It is useful for assessing the direction and absolute rate of change, but gradients of parameters with different units cannot be compared directly.

For a dimensionless comparison, the elasticity is calculated as

\[
e_i
=
g_i
\frac{x_i^\mathrm{ref}}
{f^\mathrm{ref}}
\]

The elasticity approximates the relative change in the objective caused by a relative change in the parameter near the reference design. An elasticity of \(0.5\), for example, means that a 1 % increase in the parameter is associated locally with an approximately 0.5 % increase in the objective. Elasticity is undefined when the reference parameter or reference objective is zero.

#### Interpreting local sensitivity results

Local sensitivity analysis evaluates changes in the configured scalar objective. The interpretation of an objective change depends on how the objective was defined:

* For an objective in which lower values are better (as used for optimisation), a negative objective change indicates an improvement relative to the reference point, while a positive change indicates a deterioration.
* For an objective in which higher values are better, a positive objective change indicates an improvement, while a negative change indicates a deterioration.
* A higher-is-better quantity can alternatively be multiplied by a negative factor in a linear objective. In that case, the resulting configured objective follows the lower-is-better convention that is also used for optimisation.

The gradient indicates the average direction of the configured objective response between the lower and upper parameter values:

* a positive gradient means that increasing the parameter tends to increase the configured objective;
* a negative gradient means that increasing the parameter tends to decrease the configured objective;
* a gradient close to zero indicates little average response over the evaluated interval.

Whether an increasing or decreasing objective represents an improvement depends on the objective definition. The gradient retains the units of the objective divided by the units of the parameter and should not be compared directly between parameters with different units.

The elasticity is dimensionless and describes the relative objective response in relation to the relative parameter change. Its absolute value can be used to compare the local influence of parameters with different units. A larger absolute elasticity indicates a stronger relative local influence. The sign of the elasticity describes the relationship between the parameter and the configured objective, but it may differ from the gradient sign when the reference parameter or reference objective is negative. Elasticity is undefined when the reference parameter or reference objective is zero.

The result should be interpreted only within the evaluated interval. Thresholds, operating-mode changes, and other nonlinear effects may cause the sensitivity to differ elsewhere in the parameter range. 

### Global sensitivity

Global sensitivity analysis evaluates how strongly each selected parameter influences the objective across its complete configured range. In contrast to local sensitivity analysis, all parameters may vary simultaneously. The result therefore includes both the independent influence of each parameter and effects caused by interactions between parameters.

The analysis is intended for a single scalar objective. It reuses valid results from previous parameter-study or optimisation runs when their parameter values lie within all selected bounds and their objective value is finite. Results outside the selected bounds are not used.

#### Polynomial chaos expansion

A direct variance-based sensitivity analysis would normally require a very large number of complete simulations. ReSiE therefore constructs a polynomial chaos expansion as a surrogate model. The surrogate is a computationally inexpensive approximation of the relationship between the varied parameters and the objective.

Before fitting the surrogate, every physical parameter is mapped from its configured range to the standardised interval from \(-1\) to \(1\):

\[
\xi_i
=
2
\frac{
x_i-x_i^\mathrm{lower}
}{
x_i^\mathrm{upper}-x_i^\mathrm{lower}
}
-1
\]

where \(x_i\) is the physical parameter value, \(x_i^\mathrm{lower}\) and \(x_i^\mathrm{upper}\) are its selected bounds, and \(\xi_i\) is the standardised value.

The objective is approximated by a third-degree polynomial chaos expansion:

\[
\hat{f}(\mathbf{\xi})
=
\sum_{k=0}^{K}
c_k
\Psi_k(\mathbf{\xi})
\]

where \(\hat{f}\) is the surrogate objective, \(\Psi_k\) are orthogonal multivariate polynomial terms, and \(c_k\) are coefficients fitted to the available simulation results.

The expansion contains terms that depend on individual parameters and terms that combine several parameters. Terms involving several parameters represent interactions.

For \(d\) varied parameters and a total polynomial degree of three, the number of polynomial terms is

\[
N_\mathrm{terms}
=
\binom{d+3}{3}
\]

ReSiE requires at least one more valid simulation result than the number of polynomial terms before fitting the surrogate:

\[
N_\mathrm{minimum}
=
N_\mathrm{terms}
+
1
\]

The required number of simulations therefore increases quickly when more parameters are included. For example:

| Number of parameters | Polynomial terms | Minimum valid results |
| ---: | ---: | ---: |
| 1 | 4 | 5 |
| 2 | 10 | 11 |
| 3 | 20 | 21 |
| 4 | 35 | 36 |
| 5 | 56 | 57 |
| 10 | 286 | 287 |

#### How additional runs are generated

If the available results are insufficient to fit the polynomial expansion, or if the fitted surrogate does not meet the required quality, ReSiE performs additional complete energy-system simulations.

The additional parameter combinations are generated as follows:

1. Every parameter is sampled independently from a uniform distribution.
2. Sampling takes place over the complete configured interval between its lower and upper bound.
3. The sampled standardised values are converted back to physical parameter values.
4. Every generated parameter combination is evaluated with a complete simulation.
5. After a complete batch has finished, the new results are added to the surrogate data and the polynomial expansion is fitted again.

The sampling is random. It is not directed by the optimisation algorithm and does not preferentially refine the current best result. Its purpose is to obtain broadly distributed data for estimating variance across the full parameter space. Consequently, independently repeated analyses may use different additional points and can produce slightly different indices.

When there are not yet enough results to fit the surrogate, the first additional batch is large enough to reach at least the minimum sample count. It is enlarged to use the available Julia threads where the remaining run limit permits this.

After the minimum sample count has been reached, further batches normally contain one simulation per available Julia thread. The final batch is reduced when necessary so that the configured limit for additional sensitivity runs is not exceeded.

The configured sensitivity run limit applies to newly generated sensitivity runs. Previously available results do not consume this additional-run budget.

Additional runs can be interrupted with `Ctrl+C`. In that case, ReSiE stops creating further batches and calculates the indices from the previously completed and accepted batches. Simulation results from a partially completed batch remain stored, but that incomplete batch is not included in the current surrogate fit.

#### Surrogate fitting and quality

The polynomial coefficients are fitted to the simulation results using least squares.

Surrogate quality is estimated by leave-one-out cross-validation. Conceptually, each result is predicted as if it had not been used to fit the surrogate. This tests how well the surrogate predicts simulation results rather than only how closely it reproduces its training data.

The relative root mean square error is calculated from the cross-validated residuals and normalised by the standard deviation of the simulated objective:

\[
\mathrm{RMSE}_\mathrm{rel}
=
\frac{
\sqrt{
\frac{1}{n}
\sum_{j=1}^{n}
\left(
f_j-\hat{f}_{-j}
\right)^2
}
}{
\mathrm{std}(f)
}
\]

where \(f_j\) is the simulated objective and \(\hat{f}_{-j}\) is its cross-validated surrogate prediction.

A relative RMSE close to zero indicates a good approximation. ReSiE uses the quality target

\[
\mathrm{RMSE}_\mathrm{rel}
\leq
0.1
\]

The coefficient of determination compares the cross-validated prediction errors with the total variation of the objective:

\[
R^2
=
1
-
\frac{
\sum_{j=1}^{n}
\left(
f_j-\hat{f}_{-j}
\right)^2
}{
\sum_{j=1}^{n}
\left(
f_j-\bar{f}
\right)^2
}
\]

where \(\bar{f}\) is the mean simulated objective. Values close to \(1\) indicate a good surrogate. ReSiE uses the quality target

\[
R^2
\geq
0.9
\]

Additional batches are generated while at least one of these conditions is not satisfied:

* the relative RMSE is greater than `0.1`;
* \(R^2\) is less than `0.9`.

Sampling stops when both quality targets are met, the configured maximum number of additional runs is reached, or the creation of additional runs is interrupted.

If the run limit is reached before both quality targets are met, the Sobol indices are still calculated from the available surrogate. The result should then be interpreted cautiously because the surrogate may not describe the simulation response accurately enough.

Global sensitivity cannot be calculated meaningfully when the objective is effectively constant. In that case, there is no objective variance that can be attributed to the parameters.

#### Sobol sensitivity indices

The polynomial chaos expansion separates the variance of the surrogate objective into contributions from individual parameters and parameter interactions.

The total surrogate variance is represented by all non-constant polynomial terms:

\[
V
=
\sum_{k=1}^{K}
c_k^2
\]

The first-order Sobol index of parameter \(i\) is

\[
S_i
=
\frac{V_i}{V}
\]

where \(V_i\) contains only polynomial terms that depend on parameter \(i\) and on no other parameter. It therefore represents the objective variance caused by parameter \(i\) alone.

The total-order Sobol index is

\[
S_{T_i}
=
\frac{
V_i
+
V_{i,\mathrm{interactions}}
}{
V
}
\]

It includes every polynomial term containing parameter \(i\), including terms in which it interacts with one or more other parameters.

#### Interpretation of Sobol indices

The Sobol indices \(S_i\) (S_first) and \(S_{T_i}\) (S_total) can be interpreted as follows:

* A high \(S_i\) indicates that the parameter has a strong independent influence on the objective.
* A high \(S_{T_i}\) indicates that the parameter is important either independently or through interactions.
* A large difference between \(S_{T_i}\) and \(S_i\) indicates important interactions with other parameters.
* Values close to zero indicate little influence within the selected parameter ranges.

For example, consider a parameter with

\[
S_i = 0.15
\qquad\text{and}\qquad
S_{T_i} = 0.60
\]

The parameter independently explains 15 % of the objective variance, but it participates in effects that account for 60 % of the variance. Its importance therefore arises mainly from interactions with other parameters.

First-order indices generally sum to no more than \(1\). The remaining variance is associated with interactions. Total-order indices may sum to more than \(1\) because the same interaction contributes to the total-order index of every parameter involved.

**Interpretation limits**

Sobol indices are dimensionless, but they are not fixed properties of the parameters. They depend on:

* the selected lower and upper bounds;
* the assumption that each parameter is uniformly distributed within its bounds;
* the assumption that the sampled parameters are independent;
* the accuracy of the fitted surrogate;
* the selected objective.

**Changing the parameter bounds can therefore change both the numerical indices and the ranking of parameters.** The results should always be interpreted together with the selected ranges.

The surrogate quality should be checked before ranking the parameters. If the relative RMSE is above `0.1` or \(R^2\) is below `0.9`, the indices may be unstable. Once the surrogate quality is adequate, the total-order index is the most useful measure for identifying parameters that require attention, while the difference between total-order and first-order indices indicates the importance of interactions.

Additional simulations generated for global sensitivity are stored with the other parameter-study results and can be reused by later analyses.
