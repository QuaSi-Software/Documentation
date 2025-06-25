# the timestep in seconds for the measurements
TIMESTEP_SECONDS = 900

# the timestep in seconds to which the measurements and simulation data is aggregated
AGG_STEP_SECONDS = 3600

# the leap years occuring in the measurement data, as list of strings of the full year
# e.g. ['2020', '2024']
LEAP_YEARS = ['2024']

# timezone of the measurements, e.g. 'Europe/Berlin'
TIME_ZONE = "Europe/Berlin"

# unit of energy values in the measurements, should be one of: 'kWh', 'MWh', 'GWh'
ENERGY_UNIT = "kWh"

# aggregation timestep as string in pandas time format, e.g. '1h' or '10min'
AGGREGATION = "1h"

# delimiter for CSV file of measurements
DELIMITER = ";"

# decimal character for CSV file of measurements
DECIMAL = ","

# columns that make up the timestamp. if it is from multiple, these should be in order:
# year, month, day, hour, minute, seconds
# where seconds is optional
TIMESTAMP_COLUMNS = ["timestamp"]

# if the timestamp is only one column, this format is used for parsing
TIMESTAMP_FORMAT_RAW = "%Y-%m-%d %H:%M:%S"

# dict for renaming columns after loading measurements and before further processing them
# the renamed columns should be: 'heat_out', 'el_in', 'heat_in' (optional),
# 'heat_out temp', 'heat_in temp'
# if meter values are used, 'heat_out', 'el_in', 'heat_in' can be renamed to:
# 'heat_out meter', 'el_in meter', 'heat_in meter'
RENAME_COLUMNS = {}

# flag if the measurement data should be filtered for "active" rows, meaning both heat_out
# and el_in are both non-zero
FILTER_BY_ACTIVE = True

# clipping cap in the density plot of COP for the measurement data
CLIP_CAP_MSR = 10

# clipping cap in the density plot of COP for the simulation data
CLIP_CAP_SIM = 20