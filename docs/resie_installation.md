# Installation and usage instructions
**Requirements:**

* Julia v1.8.5 or later: [https://julialang.org/downloads/](https://julialang.org/downloads/)

**Installation of ReSiE:**

1. Get a copy: `git clone git@github.com:QuaSi-Software/resie.git`
1. Switch into project directory: `cd /path/to/repo`
1. Start the julia REPL with `julia`
1. Switch to the package REPL with `]` (no enter necessary)
1. Activate the project environment: `activate .`
1. Add required packages: `add ColorSchemes Colors Dates Interpolations JSON Logging PlotlyJS`
1. (Optional) For development of ReSiE, some additional packages are necessary: `add Debugger Test`
1. Exit out of the package REPL with shortcut `Ctrl+c`
1. Exit out of the julia REPL with `exit()`

**Usage of ReSiE:**

1. Switch into project directory: `cd /path/to/resie`
1. Run the simulation with `julia --project=. src/resie-cli.jl examples/example_two_sector.json`
1. Outputs of the example projects can be found in `output/out.csv` and `output/info_dump.md`

**Usage of ReSiE with VS Code**

In Visual Studio Code, you can make configuration in the file `.vscode/launch.json` that is automatically created when you open the local ReSiE-folder with VS Code. Use the following example configure to run ReSiE directly from VS Code (copy into the `launch.json`). To run a specific input file, use the configuration "Run ReSiE from defined input file":

```JSON
{
    "version": "0.2.0",
    "configurations": [
    
        {
            "name": "Run active Julia file",
            "type": "julia",
            "request": "launch",
            "program": "${file}",
            "stopOnEntry": false,
            "cwd": "${workspaceFolder}",
            "juliaEnv": "${command:activeJuliaEnvironment}",
        },
        {
            "name": "Run ReSiE from defined input file",
            "type": "julia",
            "request": "launch",
            "stopOnEntry": false,
            "program": "path/to/resie/cli/resie-cli.jl",
            "cwd": "path/to/resie/folder/",
            "juliaEnv": "${command:activeJuliaEnvironment}",
            "args" : ["path/to/input_file.json"]
        }
    ]
}
```