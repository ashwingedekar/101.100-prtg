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


with open("server_address.txt", "r") as file:
    server_parameters = dict(line.strip().split("=") for line in file)

server_address = server_parameters.get("server")


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


upper_warning_limits = {}


for id_value in tqdm(id_values, desc="Processing IDs"):  
   
    api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&id={id_value}&subid=-1&name=limitmaxwarning&show=nohtmlencode&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
    
   
    response_upper_warning = requests.get(api_endpoint_upper_warning)
    
   
    if response_upper_warning.status_code == 200:
        
        match_upper_warning = re.search(r'<result>(\d+)</result>', response_upper_warning.text)
        if match_upper_warning:
            
            upper_warning_limits[id_value] = float(match_upper_warning.group(1)) * 8 / 1000000  

# Iterate over each ID value
for id_value in tqdm(id_values, desc="Processing IDs"):  # Use tqdm for progress bar
   
    api_endpoint = f'https://{server_address}/api/historicdata.csv?id={id_value}&avg={flags.get("avg")}&sdate={flags.get("sdate")}&edate={flags.get("edate")}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'

    response = requests.get(api_endpoint)

    df = pd.read_csv(io.StringIO(response.text))

    # Extract numeric values from the "Traffic Total (Speed)" column
    df['Traffic Total (Speed)'] = df['Traffic Total (Speed)'].str.extract(r'(\d+\.*\d*)').astype(float)
    
    selected_data = df["Traffic Total (Speed)"]
    
    selected_data.to_csv("abcd.csv", index=False)

    if flags.get("cmp") == '1':
       
        filtered_data = selected_data[selected_data > upper_warning_limits.get(id_value, 0)]

        if not filtered_data.empty:
            
            device_name_endpoint = f'https://{server_address}/api/getsensordetails.json?id={id_value}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
            
            # Make the API request to get device name
            device_name_response = requests.get(device_name_endpoint)
            
            if device_name_response.status_code == 200:
                
                device_name_json = device_name_response.json()
                parent_device_name = device_name_json["sensordata"]["parentdevicename"]
            else:
                parent_device_name = "Device name not available"
                
            for index, value in filtered_data.items():
                print(f"ID: {id_value}, Device Name: {parent_device_name}, Date: {df.loc[index, 'Date Time']}, Traffic Total: {value}")
        else:
            print(f"No data found exceeding the upper warning limit for ID: {id_value}")
output_data = []

# Iterate over each ID value
for id_value in tqdm(id_values, desc="Processing IDs"):
    # Your existing code here ...

    # If filtered_data is not empty, append the relevant information to the output_data list
    if not filtered_data.empty:
        for index, value in filtered_data.items():
            output_data.append({
                "ID": id_value,
                "Device Name": parent_device_name,
                "Date": df.loc[index, 'Date Time'],
                "Traffic Total": value
            })

# Convert the output_data list to a DataFrame
output_df = pd.DataFrame(output_data)

# Save the DataFrame to an Excel file
output_df.to_excel("UpperWarning.xlsx", index=False)