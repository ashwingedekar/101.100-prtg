import os
import requests
import pandas as pd
from io import StringIO
import warnings
from datetime import datetime
import re
from tqdm import tqdm  # Import tqdm library
import io


warnings.filterwarnings("ignore", category=DeprecationWarning)

# Read server address from the configuration file
with open("server_address.txt", "r") as file:
    server_parameters = dict(line.strip().split("=") for line in file)

server_address = server_parameters.get("server")

# Read flags from the configuration file
flags = {}
id_prefix = 'id'
id_values = []

with open("min_max_flags.txt", "r") as file:
    for line in file:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=")
            if key.startswith(id_prefix):
                id_values.append(value)
            else:
                flags[key] = value

# Initialize dictionary to store upper warning limits
upper_warning_limits = {}

# Iterate over each ID value
for id_value in tqdm(id_values, desc="Processing IDs"):  # Use tqdm for progress bar
    # Construct the API endpoint URL to get upper warning limit
    api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&id={id_value}&subid=-1&name=limitmaxwarning&show=nohtmlencode&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
    
    # Make the API request to get upper warning limit
    response_upper_warning = requests.get(api_endpoint_upper_warning)
    
    # Check if the request was successful
    if response_upper_warning.status_code == 200:
        # Extract upper warning limit from the response
        match_upper_warning = re.search(r'<result>(\d+)</result>', response_upper_warning.text)
        if match_upper_warning:
            # Convert bytes to megabits and store in the dictionary
            upper_warning_limits[id_value] = float(match_upper_warning.group(1)) * 8 / 1000000  

# Iterate over each ID value
for id_value in tqdm(id_values, desc="Processing IDs"):  # Use tqdm for progress bar
    # Construct the API endpoint URL to get historic data
    api_endpoint = f'https://{server_address}/api/historicdata.csv?id={id_value}&avg={flags.get("avg")}&sdate={flags.get("sdate")}&edate={flags.get("edate")}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'

    # Make the API request to get historic data
    response = requests.get(api_endpoint)

    # Read the CSV data into a DataFrame
    df = pd.read_csv(io.StringIO(response.text))

    # Extract numerical values from "Traffic Total (Speed)" column
    selected_data = df["Traffic Total (Speed)"].str.extract(r'(\d+\.\d+)').astype(float)
    
    # Check if cmp is equal to 1 in the min_max_flags.txt file
    if flags.get("cmp") == '1':
        # Filter rows where "Traffic Total (Speed)" exceeds the upper warning limit
        filtered_data = selected_data[selected_data[0] > upper_warning_limits.get(id_value, 0)]

        # If there are any rows matching the condition
        if not filtered_data.empty:
            # Construct the API endpoint URL to get device name
            device_name_endpoint = f'https://{server_address}/api/getsensordetails.json?id={id_value}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
            
            # Make the API request to get device name
            device_name_response = requests.get(device_name_endpoint)
            
            # Check if the request was successful
            if device_name_response.status_code == 200:
                # Extract device name from the response
                device_name_json = device_name_response.json()
                parent_device_name = device_name_json["sensordata"]["parentdevicename"]
            else:
                parent_device_name = "Device name not available"
                
            # Print corresponding ID, date, and traffic total
            for index, value in filtered_data.iterrows():
                print(f"ID: {id_value}, Device Name: {parent_device_name}, Date: {df.loc[index, 'Date Time']}, Traffic Total: {df.loc[index, 'Traffic Total (Speed)']}")
