# Installation and usage instructions
ReSiE is written in Julia and shipped as a Julia codebase. This means that it can be run on any machine that can run Julia. At the moment no compiled binaries are availabe for any platform. The following instructions help you to install and use ReSiE. There are two tools that help with creating the required input files for ReSiE and running simulations, described [in this chapter](resie_susi_simon.md).

## Requirements

* Julia, minimum v1.10.0 and tested up to v1.13.3. You can find installation instructions [here](https://julialang.org/install/). Works best using Juliaup instead of precompiled binary files.
* Internet access during installation, as the dependencies have to be downloaded

## Installation

1. Get a copy: `git clone https://github.com/QuaSi-Software/ResieQuasi.jl.git`
    * As an alternative to Git, you can also download the repository [from one of the releases on GitHub](https://github.com/QuaSi-Software/ResieQuasi.jl/releases). Download the source code as a `.zip` file and unpack it to the target directory.
2. Switch into the ReSiE root directory: `cd /path/to/resie`
3. Start the julia REPL with `julia`
4. Switch to the package REPL with `]` (no enter necessary)
5. Activate the project environment: `activate .`
    * The dot stands for the current directory and is important, because it denotes that the activated environment relates to the ReSiE directory
6. Install and precompile required packages: `instantiate`
    * This should create a file `Manifest.toml` in the ReSiE root directory and may take a while to finish
7. Exit out of the package REPL with shortcut `Ctrl+c`
8. Exit out of the julia REPL with `exit()` or shortcut `Ctrl+d`

To use profiles with a time-zone-aware datetime index beyond 2038, follow these steps:

1. Copy the zip file found at `additional_files/move_to_user_julia_scratchspaces_and_unpack.zip` from the repository to your local Julia scratchspaces directory, typically located at `C:/users/user_name/.julia/scratchspaces`.
2. Extract the content of the zip file directly into the `scratchspaces` folder. Ensure that the folder `f269a46b-ccf7-5d73-abea-4c690281aa53` is placed directly within `scratchspaces`, without any intermediate directories.

## Usage

A full description of how to use ReSiE on the examples it ships with can be found [in this chapter](resie_exemplary_energy_systems.md). In the following the standalone use via the CLI or VSCode and the use as a package is descriped.

### CLI

1. Switch to the ReSiE directory: `cd /path/to/resie`
1. Start the CLI with `julia --project=. --threads=auto src/resie-cli.jl`
    * The optional argument `--threads=auto` to the `julia` call means, that the process automatically determines the number of parallel threads (which may get executed on different cores) to use. This, in turn, causes Julia to use the available cores for computation more effectively and speeding up simulation, at the cost of other processes having fewer resources available. You can set a specific number of threads to use with `--threads=n` where `n` is the desired number.
1. In the CLI you can access the `help` command for more information or start a simulation with `run path/to/project/file.json`. If you are running multiple simulations and are only changing the project file (not any code) inbetween each run, it is very beneficial to stay within the CLI for a performance boost.
    * If instead you are changing code frequently and only want a single simulation run, you can also start the CLI with the run command and its arguments, as well as making use of an optional parameter: `julia --project=. --thread=auto src/resie-cli.jl run --exit-after-run path/to/project/file.json`. This is will start the CLI, run the simulation and then exit.
1. The outputs as well as log files can be found in the `output` folder by default. For example the examples produce a file called `output/output_plot.html` which, when opened in a browser, shows an interactive plot of simulation results.

### VSCode

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

### Package
1. Start the julia REPL with `julia --threads=auto` (usage of --threads see [description above](#CLI))
2. Switch to the package REPL with `]` (no enter necessary)
3. Add the package with `add ResieQuasi`
4. Exit out of the package REPL with shortcut `Ctrl+c`
5. Include the package in your environment `using ResieQuasi`
6. Run the simulation with `simulate("path/to/project/file.json")`
    * The function `simulate()` can also be used to control the logging. The parameter `log_level` can be set to "Auto" or one of "Debug", "Info", "BalanceWarning", "GlobalInfo", "Warn", "Error".  "Auto" sets the log_level to "Info" for a single simulation and "GlobalInfo" for multiple simulations, e.g. in a parameter study. Additionally the boolean parameters `log_to_console` and `log_to_file` define if logging should be output into the terminal or saved into the log file. Both default to `true`.