import os
import requests
import pandas as pd
from io import StringIO
import warnings
from datetime import datetime
import re
from tqdm import tqdm  # Import tqdm library

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Function to make API requests
def make_api_request(api_endpoint):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Read parameters from file
with open("server_address.txt", "r") as file:
    server_parameters = dict(line.strip().split("=") for line in file)

server_address = server_parameters.get("server")

# Read flags from the "min_max_flags.txt" file
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

# Construct API endpoints
api_endpoints = {
    "upper_warning": f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitmaxwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586',
    "upper_error": f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586',
    "lower_warning": f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitminwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586',
    "lower_error": f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitminerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
}

# Dictionary to store limits
limits = {}

# Make API requests for limits
for key, endpoint in api_endpoints.items():
    limits[key] = {}
    for id_value in id_values:
        response = make_api_request(f"{endpoint}&id={id_value}")
        if response:
            match = re.search(r'<result>(\d+)</result>', response)
            if match:
                limits[key][id_value] = int(match.group(1)) * 8 / 1000000  # Convert bytes to megabits

# Create a list to store dictionaries for each ID's data
data_list = []

# Iterate over IDs
for id_value in tqdm(id_values, desc="Processing IDs"):
    id_data = {}
    id_data["ID"] = id_value
    # Add limit data to id_data
    for limit_type, limit_values in limits.items():
        id_data.update({f"{limit_type.upper()} LIMIT": limit_values.get(id_value, "not_set")})
    
    # Construct API request for historic data
    api_endpoint = f'https://{server_address}/api/historicdata.csv?id={id_value}&avg={flags.get("avg")}&sdate={flags.get("sdate")}&edate={flags.get("edate")}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'
    response = make_api_request(api_endpoint)
    
    if response:
        try:
            # Use pandas to read the CSV data
            df = pd.read_csv(StringIO(response), na_values=['NaN', 'N/A', ''])
            # Clean up the column names (remove leading and trailing spaces)
            df.columns = df.columns.str.strip()
            # Extract specified columns
            selected_columns = ["Date Time", "Traffic Total (Speed)", "Traffic Total (Speed)(RAW)"]
            selected_data = df[selected_columns]
            # Convert selected columns to numeric type
            selected_data.loc[:, selected_columns[2:]] = selected_data[selected_columns[2:]].apply(pd.to_numeric, errors='coerce')
            # Drop rows with NaN values in "Traffic Total (Speed)(RAW)"
            selected_data = selected_data.dropna(subset=["Traffic Total (Speed)(RAW)"])
            if not selected_data.empty:
                # Find the row with the maximum "Traffic Total (Speed)(RAW)"
                max_raw_speed_row = selected_data.loc[selected_data["Traffic Total (Speed)(RAW)"].idxmax()]
                id_data["MAX SPEED"] = max_raw_speed_row['Traffic Total (Speed)']
                id_data["MAX SPEED RAW"] = max_raw_speed_row['Traffic Total (Speed)(RAW)']
                id_data["MAX SPEED DATE TIME"] = max_raw_speed_row['Date Time']
                # Find the row with the minimum "Traffic Total (Speed)(RAW)"
                min_raw_speed_row = selected_data.loc[selected_data["Traffic Total (Speed)(RAW)"].idxmin()]
                id_data["MIN SPEED"] = min_raw_speed_row['Traffic Total (Speed)']
                id_data["MIN SPEED RAW"] = min_raw_speed_row['Traffic Total (Speed)(RAW)']
                id_data["MIN SPEED DATE TIME"] = min_raw_speed_row['Date Time']
        except Exception as e:
            id_data["ERROR"] = f"Error processing CSV data for ID {id_value}: {e}"
    
    # Append ID data dictionary to the list
    data_list.append(id_data)

# Create DataFrame from data_list
df_output = pd.DataFrame(data_list)

# Display output in the terminal
for data_dict in data_list:
    print(f"ID {data_dict['ID']}:")
    print('-' * (len(f"ID {data_dict['ID']}:")))
    for key, value in data_dict.items():
        print(f"{key}: {value}")
    print("#" * 55)

# Create the output directory if it doesn't exist
output_directory = "output"
os.makedirs(output_directory, exist_ok=True)

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Construct the full file path for the output file
output_file_path = os.path.join(output_directory, f"output_{current_datetime}.csv")

# Write the DataFrame to CSV file
df_output.to_csv(output_file_path, index=False)

# Print the output file path to the terminal
print(f"\nOutput has been saved to {output_file_path}")
