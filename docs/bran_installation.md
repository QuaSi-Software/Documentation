# Installation and usage instructions
**Requirements:**

* Julia v1.7.2 or later: [https://julialang.org/downloads/](https://julialang.org/downloads/)

**Installation of bran:**

1. Get a copy: `git clone git@bran.example.com`
2. Switch into project directory: `cd /path/to/repo`

Install additional Julia-modules in working directory:

1. open julia REPL: `julia`
2. switch to julia packet manager: `]`
3. activate environment: `activate .`
4. install required external packages: `add JSON`
5. to exit packacket manager, hit `backspace`

Usage of bran:

1. Run the simulation with `julia src/Bran.jl example_two_sector.json`
