# Installation and usage instructions
**Requirements:**

* Julia, minimum v1.8.5 and tested up to v1.11.3. You can find installation instructions [here](https://julialang.org/downloads/). Works best using Juliaup instead of precompiled binary files.

**Installation of ReSiE:**

1. Get a copy: `git clone https://github.com/QuaSi-Software/resie.git`
    * Alternative to Git, you can also download the repository [from one of the releases on GitHub](https://github.com/QuaSi-Software/resie/releases).
2. Switch into the ReSiE root directory: `cd /path/to/resie`
3. Start the julia REPL with `julia`
4. Switch to the package REPL with `]` (no enter necessary)
5. Activate the local environment: `activate .`
6. Install and precompile required packages: `instantiate`. This should create a file `Manifest.toml` in the ReSiE root directory
7. Exit out of the package REPL with shortcut `Ctrl+c`
8. Exit out of the julia REPL with `exit()` or shortcut `Ctrl+d`

**Usage of ReSiE:**

A full description of how to use ReSiE on the examples it ships with can be found [in this chapter](resie_exemplary_energy_systems.md). In the following the CLI of ReSiE is described:

1. Switch to the ReSiE directory: `cd /path/to/resie`
1. Start the CLI with `julia --project=. src/resie-cli.jl`
1. In the CLI you can access the `help` command for more information or start a simulation with `run path/to/project/file.json`. If you are running multiple simulations and are only changing the project file (not any code) inbetween each run, it is very beneficial to stay within the CLI for a performance boost.
    * If instead you are changing code frequently and only want a single simulation run, you can also start the CLI with the run command and its arguments, as well as making use of an optional parameter: `julia --project=. src/resie-cli.jl run path/to/project/file.json --exit-after-run`. This is will start the CLI, run the simulation and then exit.
1. The outputs as well as log files can be found in the `output` folder by default. For example the examples produce a file called `output/output_plot.html` which, when opened in a browser, shows an interactive plot of simulation results.

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
            "args" : ["run", "path/to/input_file.json", "--exit-after-run"]
        }
    ]
}
```