import os
import requests
import pandas as pd
from io import StringIO
import warnings
from datetime import datetime
import re
from tqdm import tqdm
import io

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load server parameters from file
with open("server_address.txt", "r") as file:
    server_parameters = dict(line.strip().split("=") for line in file)

server_address = server_parameters.get("server")

flags = {}
id_prefix = 'id'
id_values = []

# Load flags from file
with open("min_max_flags.txt", "r") as file:
    for line in file:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=")
            if key.startswith(id_prefix):
                id_values.append(value)
            else:
                flags[key] = value

upper_error_limits = {}

# Retrieve upper warning limits
for id_value in tqdm(id_values, desc="Getting Error Limit For Each ID's"):  
    api_endpoint_upper_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&id={id_value}&subid=-1&name=limitmaxerror&show=nohtmlencode&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
    response_upper_error = requests.get(api_endpoint_upper_error)
    if response_upper_error.status_code == 200:
        match_upper_error = re.search(r'<result>(\d+)</result>', response_upper_error.text)
        if match_upper_error:
            upper_error_limits[id_value] = float(match_upper_error.group(1)) * 8 / 1000000  

# Prepare a list to hold output data
output_data = []

# Iterate over each ID value
for id_value in tqdm(id_values, desc="Getting Historical data For each Id's"):  
    api_endpoint = f'https://{server_address}/api/historicdata.csv?id={id_value}&avg={flags.get("avg")}&sdate={flags.get("sdate")}&edate={flags.get("edate")}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
    response = requests.get(api_endpoint)
    df = pd.read_csv(io.StringIO(response.text))
    df['Traffic Total (Speed)'] = df['Traffic Total (Speed)'].str.extract(r'(\d+\.*\d*)').astype(float)
    selected_data = df["Traffic Total (Speed)"]
    
    if flags.get("cmp") == '1':
        filtered_data = selected_data[selected_data > upper_error_limits.get(id_value, 0)]
        if not filtered_data.empty:
            device_name_endpoint = f'https://{server_address}/api/getsensordetails.json?id={id_value}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
            device_name_response = requests.get(device_name_endpoint)
            if device_name_response.status_code == 200:
                device_name_json = device_name_response.json()
                parent_device_name = device_name_json["sensordata"]["parentdevicename"]
            else:
                parent_device_name = "Device name not available"
            for index, value in filtered_data.items():
                output_data.append({
                    "ID": id_value,
                    "Device Name": parent_device_name,
                    "Date": df.loc[index, 'Date Time'],
                    "Traffic Total": value
                })
        else:
            print(f"No data found exceeding the upper Error limit for ID: {id_value}")
    else:
        print(f"No data found exceeding the upper Error limit for ID: {id_value}")

# Create a DataFrame from the output data
output_df = pd.DataFrame(output_data)

# Group the data by "Device Name" and "ID" and aggregate the traffic totals
grouped_data = output_df.groupby(["Device Name", "ID"], as_index=False)["Traffic Total"].sum()
#grouped_data = output_df.groupby(["Device Name", "ID"], as_index=False).agg({"Traffic Total": "sum"})

# Generate filename with current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"output_{current_datetime}.csv"

# Save the grouped and aggregated data to Excel
grouped_data.to_csv(output_filename, index=False)
print(f"Data saved to {output_filename}")

# Release memory
del output_data
del output_df
