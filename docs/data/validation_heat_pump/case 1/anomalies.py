"""This script reads a CSV file containing measurements from a heat pump system, processes
the data to identify anomalies, and writes the anomalies to a text file.
It checks for missing values, out-of-range values, and negative differences in meter
readings.
"""
import pandas as pd

def main():
    """Main function to read the CSV file, process the data, and identify anomalies."""
    file_path = 'measurements_all.csv'
    data = pd.read_csv(file_path, delimiter=";", decimal=",", na_values=["\\N", ""])

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)

    data['el_in diff'] = data['el_in meter'].diff()
    data['heat_in diff'] = data['heat_in meter'].diff()
    data['heat_out diff'] = data['heat_out meter'].diff()

    data = data[
        pd.isna(data['el_in meter']) |
        pd.isna(data['heat_in meter']) |
        pd.isna(data['heat_out meter']) |
        pd.isna(data['heat_out temp']) |
        pd.isna(data['heat_in temp']) |
        (data['heat_in temp'] < 1) |
        (data['heat_in temp'] > 20) |
        (data['heat_out temp'] < 20) |
        (data['heat_out temp'] > 80) |
        (data['el_in diff'] < 0) |
        (data['heat_in diff'] < 0) |
        (data['heat_out diff'] < 0) |
        (data['el_in diff'] > 100) |
        (data['heat_in diff'] > 100) |
        (data['heat_out diff'] > 100)
    ]

    with open('anomalies.txt', 'w', encoding="utf-8") as file:
        file.write(data.to_string())

main()
