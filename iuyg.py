import os
import requests
import pandas as pd
from io import StringIO
import warnings
from datetime import datetime
import re
from tqdm import tqdm  # Import tqdm library

warnings.filterwarnings("ignore", category=DeprecationWarning)

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

# Construct API endpoints for upper and lower error and warning limits for all IDs
# Define other API endpoints
sensor_details_api_endpoint = 'https://tp-prtg-101-100.comtelindia.com:10443/api/getsensordetails.json'
api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitmaxwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
api_endpoint_upper_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
api_endpoint_lower_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitminwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
api_endpoint_lower_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=-1&name=limitminerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'

discard_in_api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=12&name=limitmaxwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
discard_in_api_endpoint_upper_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=12&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
discard_in_api_endpoint_lower_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=12&name=limitminwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
discard_in_api_endpoint_lower_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=12&name=limitminerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'

discard_out_api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=13&name=limitmaxwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
discard_out_api_endpoint_upper_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=13&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
discard_out_api_endpoint_lower_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=13&name=limitminwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
discard_out_api_endpoint_lower_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=13&name=limitminerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'

error_in_api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=10&name=limitmaxwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
error_in_api_endpoint_upper_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=10&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
error_in_api_endpoint_lower_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=10&name=limitminwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
error_in_api_endpoint_lower_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=10&name=limitminerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'

error_out_api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=11&name=limitmaxwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
error_out_api_endpoint_upper_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=11&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
error_out_api_endpoint_lower_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=11&name=limitminwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
error_out_api_endpoint_lower_error = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&subid=11&name=limitminerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'



# Create dictionaries to store upper and lower error and warning limits for each ID
upper_warning_limits = {}
upper_error_limits = {}
lower_warning_limits = {}
lower_error_limits = {}

discard_in_upper_warning_limits = {}
discard_in_upper_error_limits = {}
discard_in_lower_warning_limits = {}
discard_in_lower_error_limits = {}

discard_out_upper_warning_limits = {}
discard_out_upper_error_limits = {}
discard_out_lower_warning_limits = {}
discard_out_lower_error_limits = {}

error_in_upper_warning_limits = {}
error_in_upper_error_limits = {}
error_in_lower_warning_limits = {}
error_in_lower_error_limits = {}

error_out_upper_warning_limits = {}
error_out_upper_error_limits = {}
error_out_lower_warning_limits = {}
error_out_lower_error_limits = {}

# Create tqdm instance for progress indication
progress_bar = tqdm(total=len(id_values), desc="Fetching limits for each ID")

# Make the API requests for each ID to get the limits
for id_value in id_values:
    response_upper_warning = requests.get(f"{api_endpoint_upper_warning}&id={id_value}")
    # Add other API requests here...

    # Update the progress bar
    progress_bar.update(1)

# Close the progress bar
progress_bar.close()

# Create dictionaries to store upper and lower error and warning limits for each ID
# Define other dictionaries here...

# Define other dictionaries here...

# Create a list to store dictionaries for each ID's data
data_list = []

# Construct API requests for each ID
for id_value in tqdm(id_values, desc="Processing IDs"):  # Use tqdm for progress bar
    # Construct the API endpoint URL using the extracted parameters
    api_endpoint = f'https://{server_address}/api/historicdata.csv?id={id_value}&avg={flags.get("avg")}&sdate={flags.get("sdate")}&edate={flags.get("edate")}&username={server_parameters.get("username")}&passhash={server_parameters.get("passhash")}'

    # Make the API request
    response = requests.get(api_endpoint)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        id_data = {
            "ID": id_value,
            "MAX SPEED": None,
            "MAX SPEED RAW": None,
            "MAX SPEED DATE TIME": None,
            "MIN SPEED": None,
            "MIN SPEED RAW": None,
            "MIN SPEED DATE TIME": None,
            "THRESHOLD MESSAGE (MAX)": None,
            "THRESHOLD MESSAGE (MIN)": None,
            "DISCARD IN UPPER ERROR LIMIT": None,
            "DISCARD IN LOWER ERROR LIMIT": None,
            "DISCARD IN UPPER WARNING LIMIT": None,
            "DISCARD IN LOWER WARNING LIMIT": None,
            "DISCARD OUT UPPER ERROR LIMIT": None,
            "DISCARD OUT LOWER ERROR LIMIT": None,
            "DISCARD OUT UPPER WARNING LIMIT": None,
            "DISCARD OUT LOWER WARNING LIMIT": None,
            "ERROR IN UPPER ERROR LIMIT": None,
            "ERROR IN LOWER ERROR LIMIT": None,
            "ERROR IN UPPER WARNING LIMIT": None,
            "ERROR IN LOWER WARNING LIMIT": None,
            "ERROR OUT UPPER ERROR LIMIT": None,
            "ERROR OUT LOWER ERROR LIMIT": None,
            "ERROR OUT UPPER WARNING LIMIT": None,
            "ERROR OUT LOWER WARNING LIMIT": None,
            "TRAFFIC TOTAL UPPER ERROR LIMIT": None,
            "TRAFFIC TOTAL LOWER ERROR LIMIT": None,
            "TRAFFIC TOTAL UPPER WARNING LIMIT": None,
            "TRAFFIC TOTAL LOWER WARNING LIMIT": None
        }

        try:
            # Use pandas to read the CSV data
            df = pd.read_csv(StringIO(response.text), na_values=['NaN', 'N/A', ''])

            # Clean up the column names (remove leading and trailing spaces)
            df.columns = df.columns.str.strip()

            # Extract specified columns along with "Date Time", "Traffic Total (Speed)", "Traffic Total (Speed)(RAW)", "Discards In (Speed)", "Discards Out (Speed)", "Errors In (Speed)", and "Errors Out (Speed)"
            selected_columns = ["Date Time", "Traffic Total (Speed)", "Traffic Total (Speed)(RAW)", "Discards In (Speed)", "Discards Out (Speed)", "Errors In (Speed)", "Errors Out (Speed)"]
            selected_data = df[selected_columns]

            # Convert selected columns to numeric type
            selected_data.loc[:, selected_columns[2:]] = selected_data[selected_columns[2:]].apply(pd.to_numeric, errors='coerce')

            # Drop rows with NaN values in "Traffic Total (Speed)(RAW)"
            selected_data = selected_data.dropna(subset=["Traffic Total (Speed)(RAW)"])

            # Check if the DataFrame is not empty
            if not selected_data.empty:
                selected_data["Traffic Total (Speed)"] = selected_data["Traffic Total (Speed)"].fillna("< 0.01")

                if flags.get("max") == '1':
                    # Find the row with the maximum "Traffic Total (Speed)(RAW)"
                    max_raw_speed_row = selected_data.loc[selected_data["Traffic Total (Speed)(RAW)"].idxmax()]
                    id_data["MAX SPEED"] = max_raw_speed_row['Traffic Total (Speed)']
                    id_data["MAX SPEED RAW"] = max_raw_speed_row['Traffic Total (Speed)(RAW)']
                    id_data["MAX SPEED DATE TIME"] = max_raw_speed_row['Date Time']

                    # Check if thr=1 and upper error limit and warning limit are available for the current ID
                    if flags.get("thr") == '1' and id_value in upper_error_limits and id_value in upper_warning_limits:
                        max_speed_value = float(max_raw_speed_row['Traffic Total (Speed)'])

                        if max_speed_value >= upper_error_limits[id_value]:
                            id_data["ERROR OUT UPPER ERROR LIMIT"] = max_speed_value
                        elif max_speed_value >= upper_warning_limits[id_value]:
                            id_data["ERROR OUT UPPER WARNING LIMIT"] = max_speed_value
                    elif flags.get("thr") == '1' and id_value in upper_warning_limits:
                        max_speed_value = float(max_raw_speed_row['Traffic Total (Speed)'])

                        if max_speed_value >= upper_warning_limits[id_value]:
                            id_data["ERROR OUT UPPER WARNING LIMIT"] = max_speed_value

                if flags.get("min") == '1':
                    # Find the row with the minimum "Traffic Total (Speed)(RAW)"
                    min_raw_speed_row = selected_data.loc[selected_data["Traffic Total (Speed)(RAW)"].idxmin()]
                    id_data["MIN SPEED"] = min_raw_speed_row['Traffic Total (Speed)']
                    id_data["MIN SPEED RAW"] = min_raw_speed_row['Traffic Total (Speed)(RAW)']
                    id_data["MIN SPEED DATE TIME"] = min_raw_speed_row['Date Time']

                    # Check if thr=1 and lower error limit and warning limit are available for the current ID
                    if flags.get("thr") == '1' and id_value in lower_error_limits and id_value in lower_warning_limits:
                        min_speed_value = float(min_raw_speed_row['Traffic Total (Speed)'])

                        if min_speed_value <= lower_error_limits[id_value]:
                            id_data["ERROR OUT LOWER ERROR LIMIT"] = min_speed_value
                        elif min_speed_value <= lower_warning_limits[id_value]:
                            id_data["ERROR OUT LOWER WARNING LIMIT"] = min_speed_value
                    elif flags.get("thr") == '1' and id_value in lower_warning_limits:
                        min_speed_value = float(min_raw_speed_row['Traffic Total (Speed)'])

                        if min_speed_value <= lower_warning_limits[id_value]:
                            id_data["ERROR OUT LOWER WARNING LIMIT"] = min_speed_value

                if flags.get("thr") == '1':
                    # Check if upper and lower error and warning limits are available for the current ID
                    if id_value in upper_error_limits and id_value in lower_error_limits and id_value in upper_warning_limits and id_value in lower_warning_limits:
                        max_speed_value = float(max_raw_speed_row['Traffic Total (Speed)'])
                        min_speed_value = float(min_raw_speed_row['Traffic Total (Speed)'])

                        if max_speed_value >= upper_error_limits[id_value]:
                            id_data["TRAFFIC TOTAL UPPER ERROR LIMIT"] = max_speed_value
                        elif min_speed_value <= lower_error_limits[id_value]:
                            id_data["TRAFFIC TOTAL LOWER ERROR LIMIT"] = min_speed_value

                        if max_speed_value >= upper_warning_limits[id_value]:
                            id_data["TRAFFIC TOTAL UPPER WARNING LIMIT"] = max_speed_value
                        elif min_speed_value <= lower_warning_limits[id_value]:
                            id_data["TRAFFIC TOTAL LOWER WARNING LIMIT"] = min_speed_value

                # Extract threshold messages from the description
                description = df.iloc[0]['Message']
                if description:
                    threshold_messages = re.findall(r'Threshold \d+\.\s(.*?)\.\s', description)
                    if len(threshold_messages) >= 1:
                        id_data["THRESHOLD MESSAGE (MAX)"] = threshold_messages[0]
                    if len(threshold_messages) >= 2:
                        id_data["THRESHOLD MESSAGE (MIN)"] = threshold_messages[1]

                # Extract discard, error, and threshold data
                discard_data = re.findall(r'Discards\s\(In\/Out\)\:\s(\d+)\/(\d+)', description)
                if discard_data:
                    id_data["DISCARD IN UPPER ERROR LIMIT"] = discard_data[0][0]
                    id_data["DISCARD OUT UPPER ERROR LIMIT"] = discard_data[0][1]

                error_data = re.findall(r'Errors\s\(In\/Out\)\:\s(\d+)\/(\d+)', description)
                if error_data:
                    id_data["ERROR IN UPPER ERROR LIMIT"] = error_data[0][0]
                    id_data["ERROR OUT UPPER ERROR LIMIT"] = error_data[0][1]

                # Append the data dictionary to the data list
                data_list.append(id_data)

        except Exception as e:
            print(f"Error processing ID {id_value}: {e}")

# Create a DataFrame from the data list
df_final = pd.DataFrame(data_list)

# Read device details from API
device_details_response = requests.get(sensor_details_api_endpoint)
device_details_json = device_details_response.json()

# Construct a dictionary to map sensor ID to device name
sensor_to_device_map = {}
for sensor in device_details_json.get("sensordetails", []):
    sensor_id = sensor.get("objid")
    device_name = sensor.get("device")
    sensor_to_device_map[sensor_id] = device_name

# Add a new column for device name based on sensor ID
df_final['Device Name'] = df_final['ID'].map(sensor_to_device_map)

# Save DataFrame to Excel
excel_file_name = f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
df_final.to_excel(excel_file_name, index=False)

print(f"Excel file saved: {excel_file_name}")
