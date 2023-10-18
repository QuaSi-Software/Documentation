# GenSim User manual
**Requirements:**

* Julia v1.8.5 or later: [https://julialang.org/downloads/](https://julialang.org/downloads/)

**Installation of resie:**

1. Get a copy: `git clone git@github.com:QuaSi-Software/resie.git`
1. Switch into project directory: `cd /path/to/repo`
1. Start the julia REPL with `julia`
1. Switch to the package REPL with `]` (no enter necessary)
1. Activate the project environment: `activate .`
1. Add required packages: `add ColorSchemes Debugger Infiltrator JSON PlotlyJS ResumableFunctions Test`
1. Exit out of the package REPL with shortcut `Ctrl+c`
1. Exit out of the julia REPL with `exit()`

**Usage of resie:**

1. Switch into project directory: `cd /path/to/resie`
1. Run the simulation with `julia --project=. src/resie-cli.jl examples/example_two_sector.json`
1. Outputs of the example projects can be found in `output/out.csv` and `output/info_dump.md`

![General System chart of a heat pump](fig/221018_HeatPump_system_chart.svg)
