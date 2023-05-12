# Installation and usage instructions
**Requirements:**

* Julia v1.7.2 or later: [https://julialang.org/downloads/](https://julialang.org/downloads/)

**Installation of resie:**

1. Get a copy: `git clone git@resie.example.com`
2. Switch into project directory: `cd /path/to/repo`

Install additional Julia-modules in working directory:

1. open julia REPL: `julia`
2. switch to julia packet manager: `]`
3. activate environment: `activate .`
4. install required external packages: 
      - `add ColorSchemes`
      - `add Debugger`
      - `add Infiltrator`
      - `add JSON`
      - `add PlotlyJS`
      - `add ResumableFunctions`
      - `add Test`
5. to exit packet manager, hit `backspace`

Usage of resie:

1. Run the simulation with `julia src/Resie.jl example_two_sector.json`
