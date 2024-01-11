# Logging

In the following, the logging capabilities of ReSiE are described. 

## Logging from user's perspective

ReSiE creates logging messages in different logging category, each with their own color in the console. These are:

 - **Debug:** Debug messages are for debugging purposes and are not used so far in ReSiE. They can be activated in the sourcecode (see next chapter)
 - **Info:** Information messages for information purpose only, including project loading information or simulation states. These messages can be used to ensure the engine is interpreting the inputs correctly. 
 - **BalanceWarning:** This logging levels contains only balance warnings. In every simulation time step, ReSiE checks the energy balances at all busses and interfaces. If a balance mismatch is detected, e.g due to an unmet demand, this will be logged into this category. Note that these are written to a separate file!
 - **Warning:** Warnings are important messages of the simulation engine. They should be checked by the user in order to make sure that the engine does the requested job. This can include assumptions made by ReSiE due to missing information.
 - **Error:** Errors are severe errors within the simulation that usually causes the simulation to be stopped. This can include a corrupt input file.

All logging messages are written to the console and into logging files. Except of BalanceWarning, the log messages are saved in `outputs/logfile_general.log`, while the balance warnings are written to the separate file `outputs/logfile_balanceWarn.log`, so that the rest of the logging outputs is not being buried. Note that the logfiles are written at the end of the simulation and after each log with error-level.

## Logging from developer's perspective

The different logging levels can be accessed in the code using the macros, e.g. `@info "This is an info log message"`. Each logging category corresponts to an internal logging level. In ReSiE, the standard library "Logging" from Julia is used, but extended by custom log level(s). As this is not directly supported from the Logging-Module, some workarounds had to be made. 

An overview of the available logging categories and the corresponding logging levels of the Logging-Modules are given in the table below: 

| logging category   |  macro name   |  internal logging level                                  |
|--------------------|---------------|----------------------------------------------------------|
| Debug              | @debug        | Logging.LogLevel(-1000)                                  |
| Info               | @info         | Logging.LogLevel(    0)                                  |
| BalanceWarning     | @balanceWarn  | Logging.LogLevel(  500)  <-- this is a custom log level! |
| Warn               | @warn         | Logging.LogLevel( 1000)                                  |
| Error              | @error        | Logging.LogLevel( 2000)                                  |
 
Custom logging functionalities can be defined in the `resie-cli.jl`. Here, the output file paths for the log files and the minimum logging level for the output can be set. By default, the minimum log level is the info-level, so debug-messages are not logged. Additionally, logging to console or to the logfiles can be completely deactivated, like it is done for the automated tests. 

Custom logging levels can be defined in the Resie_Logger module `resie_logger.jl`. See the description in the module for how to set up further custom logging levels.