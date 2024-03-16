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



#https://tp-prtg-101-100.comtelindia.com:10443/api/getobjectproperty.htm?id=10705&subtype=channel&subid=12&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586


# Create tqdm instance for progress indication
progress_bar = tqdm(total=len(id_values), desc="Fetching limits for each ID")

# Make the API requests for each ID to get the limits
for id_value in id_values:
    response_upper_warning = requests.get(f"{api_endpoint_upper_warning}&id={id_value}")
    response_upper_error = requests.get(f"{api_endpoint_upper_error}&id={id_value}")
    response_lower_warning = requests.get(f"{api_endpoint_lower_warning}&id={id_value}")
    response_lower_error = requests.get(f"{api_endpoint_lower_error}&id={id_value}")
    response_discard_in_upper_warning = requests.get(f"{discard_in_api_endpoint_upper_warning}&id={id_value}")
    response_discard_in_upper_error = requests.get(f"{discard_in_api_endpoint_upper_error}&id={id_value}")
    response_discard_in_lower_warning = requests.get(f"{discard_in_api_endpoint_lower_warning}&id={id_value}")
    response_discard_in_lower_error = requests.get(f"{discard_in_api_endpoint_lower_error}&id={id_value}")
    response_discard_out_upper_warning = requests.get(f"{discard_out_api_endpoint_upper_warning}&id={id_value}")
    response_discard_out_upper_error = requests.get(f"{discard_out_api_endpoint_upper_error}&id={id_value}")
    response_discard_out_lower_warning = requests.get(f"{discard_out_api_endpoint_lower_warning}&id={id_value}")
    response_discard_out_lower_error = requests.get(f"{discard_out_api_endpoint_lower_error}&id={id_value}")
    response_error_in_upper_warning = requests.get(f"{error_in_api_endpoint_upper_warning}&id={id_value}")
    response_error_in_upper_error = requests.get(f"{error_in_api_endpoint_upper_error}&id={id_value}")
    response_error_in_lower_warning = requests.get(f"{error_in_api_endpoint_lower_warning}&id={id_value}")
    response_error_in_lower_error = requests.get(f"{error_in_api_endpoint_lower_error}&id={id_value}")
    response_error_out_upper_warning = requests.get(f"{error_out_api_endpoint_upper_warning}&id={id_value}")
    response_error_out_upper_error = requests.get(f"{error_out_api_endpoint_upper_error}&id={id_value}")
    response_error_out_lower_warning = requests.get(f"{error_out_api_endpoint_lower_warning}&id={id_value}")
    response_error_out_lower_error = requests.get(f"{error_out_api_endpoint_lower_error}&id={id_value}")
    
    # Traffic total 
    if response_upper_warning.status_code == 200:
        match_upper_warning = re.search(r'<result>(\d+)</result>', response_upper_warning.text)
        if match_upper_warning:
            upper_warning_limits[id_value] = int(match_upper_warning.group(1)) * 8 / 1000000  # Convert bytes to megabits
    


    if response_upper_error.status_code == 200:
       match_upper_error = re.search(r'<result>(\d+)</result>', response_upper_error.text)
       if match_upper_error:
          upper_error_limits[id_value] = int(match_upper_error.group(1)) * 8 / 1000000  # Convert bytes to megabits
    

    if response_lower_warning.status_code == 200:
        match_lower_warning = re.search(r'<result>(\d+)</result>', response_lower_warning.text)
        if match_lower_warning:
            lower_warning_limits[id_value] = int(match_lower_warning.group(1)) * 8 / 1000000  # Convert bytes to megabits

    if response_lower_error.status_code == 200:
        match_lower_error = re.search(r'<result>(\d+)</result>', response_lower_error.text)
        if match_lower_error:
            lower_error_limits[id_value] = int(match_lower_error.group(1)) * 8 / 1000000  # Convert bytes to megabits
    
     # discord in
    if response_discard_in_upper_warning.status_code == 200:
        match_discard_in_upper_warning = re.search(r'<result>(\d+)</result>', response_discard_in_upper_warning.text)
        if match_discard_in_upper_warning:
            discard_in_upper_warning_limits[id_value] = match_discard_in_upper_warning.group(1) 

    if response_discard_in_upper_error.status_code == 200:
       match_discard_in_upper_error = re.search(r'<result>(\d+)</result>', response_discard_in_upper_error.text)
       if match_discard_in_upper_error:
        discard_in_upper_error_limits[id_value] = match_discard_in_upper_error.group(1)


    if response_discard_in_lower_warning.status_code == 200:
        match_discard_in_lower_warning = re.search(r'<result>(\d+)</result>', response_discard_in_lower_warning.text)
        if match_discard_in_lower_warning:
            discard_in_lower_warning_limits[id_value] = match_discard_in_lower_warning.group(1)  

    if response_discard_in_lower_error.status_code == 200:
        match_discard_in_lower_error = re.search(r'<result>(\d+)</result>', response_discard_in_lower_error.text)
        if match_discard_in_lower_error:
            discard_in_lower_error_limits[id_value] = match_discard_in_lower_error.group(1)
    
   # discord out
    if response_discard_out_upper_warning.status_code == 200:
        match_discard_out_upper_warning = re.search(r'<result>(\d+)</result>', response_discard_out_upper_warning.text)
        if match_discard_out_upper_warning:
            discard_out_upper_warning_limits[id_value] = match_discard_out_upper_warning.group(1) 

    if response_discard_out_upper_error.status_code == 200:
       match_discard_out_upper_error = re.search(r'<result>(\d+)</result>', response_discard_out_upper_error.text)
       if match_discard_out_upper_error:
        discard_out_upper_error_limits[id_value] = match_discard_out_upper_error.group(1)


    if response_discard_out_lower_warning.status_code == 200:
        match_discard_out_lower_warning = re.search(r'<result>(\d+)</result>', response_discard_out_lower_warning.text)
        if match_discard_out_lower_warning:
            discard_out_lower_warning_limits[id_value] = match_discard_out_lower_warning.group(1)  

    if response_discard_out_lower_error.status_code == 200:
        match_discard_out_lower_error = re.search(r'<result>(\d+)</result>', response_discard_out_lower_error.text)
        if match_discard_out_lower_error:
            discard_out_lower_error_limits[id_value] = match_discard_out_lower_error.group(1)

    # Error IN
    
    if response_error_in_upper_warning.status_code == 200:
        match_error_in_upper_warning = re.search(r'<result>(\d+)</result>', response_error_in_upper_warning.text)
        if match_error_in_upper_warning:
            error_in_upper_warning_limits[id_value] = match_error_in_upper_warning.group(1) 

    if response_error_in_upper_error.status_code == 200:
       match_error_in_upper_error = re.search(r'<result>(\d+)</result>', response_error_in_upper_error.text)
       if match_error_in_upper_error:
        error_in_upper_error_limits[id_value] = match_error_in_upper_error.group(1)


    if response_error_in_lower_warning.status_code == 200:
        match_error_in_lower_warning = re.search(r'<result>(\d+)</result>', response_error_in_lower_warning.text)
        if match_error_in_lower_warning:
            error_in_lower_warning_limits[id_value] = match_error_in_lower_warning.group(1)  

    if response_error_in_lower_error.status_code == 200:
        match_error_in_lower_error = re.search(r'<result>(\d+)</result>', response_error_in_lower_error.text)
        if match_error_in_lower_error:
            error_in_lower_error_limits[id_value] = match_error_in_lower_error.group(1)
    

    # Error OUT 
    
    if response_error_out_upper_warning.status_code == 200:
        match_error_out_upper_warning = re.search(r'<result>(\d+)</result>', response_error_out_upper_warning.text)
        if match_error_out_upper_warning:
            error_out_upper_warning_limits[id_value] = match_error_out_upper_warning.group(1) 

    if response_error_out_upper_error.status_code == 200:
       match_error_out_upper_error = re.search(r'<result>(\d+)</result>', response_error_out_upper_error.text)
       if match_error_out_upper_error:
        error_out_upper_error_limits[id_value] = match_error_out_upper_error.group(1)


    if response_error_out_lower_warning.status_code == 200:
        match_error_out_lower_warning = re.search(r'<result>(\d+)</result>', response_error_out_lower_warning.text)
        if match_error_out_lower_warning:
            error_out_lower_warning_limits[id_value] = match_error_out_lower_warning.group(1)  

    if response_error_out_lower_error.status_code == 200:
        match_error_out_lower_error = re.search(r'<result>(\d+)</result>', response_error_out_lower_error.text)
        if match_error_out_lower_error:
            error_out_lower_error_limits[id_value] = match_error_out_lower_error.group(1)


    
    # Update the progress bar
    progress_bar.update(1)


# Close the progress bar
progress_bar.close()

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
          #  "THRESHOLD MESSAGE (MAX)": None,
          #  "THRESHOLD MESSAGE (MIN)": None,
          #  "DISCARD IN UPPER ERROR LIMIT": discard_in_upper_error_limits.get(id_value, "not_set"),
          #  "DISCARD IN LOWER ERROR LIMIT": discard_in_lower_error_limits.get(id_value, "not_set"),
          #  "DISCARD IN UPPER WARNING LIMIT": discard_in_upper_warning_limits.get(id_value, "not_set"),
          #  "DISCARD IN LOWER WARNING LIMIT": discard_in_lower_warning_limits.get(id_value, "not_set"),
          #  "DISCARD OUT UPPER ERROR LIMIT": discard_out_upper_error_limits.get(id_value, "not_set"),
          #  "DISCARD OUT LOWER ERROR LIMIT": discard_out_lower_error_limits.get(id_value, "not_set"),
          #  "DISCARD OUT UPPER WARNING LIMIT": discard_out_upper_warning_limits.get(id_value, "not_set"),
          #  "DISCARD OUT LOWER WARNING LIMIT": discard_out_lower_warning_limits.get(id_value, "not_set"),
            "ERROR IN UPPER ERROR LIMIT": error_in_upper_error_limits.get(id_value, "not_set"),
            "ERROR IN LOWER ERROR LIMIT": error_in_lower_error_limits.get(id_value, "not_set"),
            "ERROR IN UPPER WARNING LIMIT": error_in_upper_warning_limits.get(id_value, "not_set"),
            "ERROR IN LOWER WARNING LIMIT": error_in_lower_warning_limits.get(id_value, "not_set"),
            "ERROR OUT UPPER ERROR LIMIT": error_out_upper_error_limits.get(id_value, "not_set"),
            "ERROR OUT LOWER ERROR LIMIT": error_out_lower_error_limits.get(id_value, "not_set"),
            "ERROR OUT UPPER WARNING LIMIT": error_out_upper_warning_limits.get(id_value, "not_set"),
            "ERROR OUT LOWER WARNING LIMIT": error_out_lower_warning_limits.get(id_value, "not_set"),
            "TRAFFIC TOTAL UPPER ERROR LIMIT": upper_error_limits.get(id_value, "not_set"),
            "TRAFFIC TOTAL LOWER ERROR LIMIT": lower_error_limits.get(id_value, "not_set"),
            "TRAFFIC TOTAL UPPER WARNING LIMIT": upper_warning_limits.get(id_value, "not_set"),
            "TRAFFIC TOTAL LOWER WARNING LIMIT": lower_warning_limits.get(id_value, "not_set")
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
                        max_speed_value = float(max_raw_speed_row['Traffic Total (Speed)'].split()[0])

                        upper_error_limit = upper_error_limits[id_value]
                        upper_warning_limit = upper_warning_limits[id_value]

                        if max_speed_value > upper_error_limit and max_speed_value <= upper_warning_limit:
                            id_data["THRESHOLD MESSAGE (MAX)"] = f"MAX SPEED for ID {id_value} is within Upper Error Limit({upper_error_limit} Mbit/s) and Upper Warning Limit({upper_warning_limit} Mbit/s)"
                        elif max_speed_value <= upper_error_limit and max_speed_value > upper_warning_limit:
                            id_data["THRESHOLD MESSAGE (MAX)"] = f"MAX SPEED for ID {id_value} crosses Upper Warning Limit({upper_warning_limit} Mbit/s) but is within Upper Error Limit({upper_error_limit} Mbit/s)"
                        elif max_speed_value <= upper_error_limit and max_speed_value <= upper_warning_limit:
                            id_data["THRESHOLD MESSAGE (MAX)"] = f"MAX SPEED for ID {id_value} is within both Upper Error Limit({upper_error_limit} Mbit/s) and Upper Warning Limit({upper_warning_limit} Mbit/s)"
                        else:
                            id_data["THRESHOLD MESSAGE (MAX)"] = f"MAX SPEED for ID {id_value} is above both Upper Error Limit({upper_error_limit} Mbit/s) and Upper Warning Limit({upper_warning_limit} Mbit/s)"
                    else:
                        id_data["THRESHOLD MESSAGE (MAX)"] = f"not_set"

                # Find the row with the minimum "Traffic Total (Speed)(RAW)"
                min_raw_speed_row = selected_data.loc[selected_data["Traffic Total (Speed)(RAW)"].idxmin()]
                id_data["MIN SPEED"] = min_raw_speed_row['Traffic Total (Speed)']
                id_data["MIN SPEED RAW"] = min_raw_speed_row['Traffic Total (Speed)(RAW)']
                id_data["MIN SPEED DATE TIME"] = min_raw_speed_row['Date Time']

                # Check if thr=1 and lower error limit and warning limit are available for the current ID
                if flags.get("thr") == '1' and id_value in lower_error_limits and id_value in lower_warning_limits:
                    min_speed_value = float(min_raw_speed_row['Traffic Total (Speed)'].split()[0])

                    lower_error_limit = lower_error_limits[id_value]
                    lower_warning_limit = lower_warning_limits[id_value]

                    if min_speed_value < lower_error_limit:
                        id_data["THRESHOLD MESSAGE (MIN)"] = f"MIN SPEED for ID {id_value} is below Lower Error Limit({lower_error_limit} Mbit/s)"
                    elif min_speed_value >= lower_error_limit and min_speed_value < lower_warning_limit:
                        id_data["THRESHOLD MESSAGE (MIN)"] = f"MIN SPEED for ID {id_value} is within Lower Error Limit({lower_error_limit} Mbit/s) and Lower Warning Limit({lower_warning_limit} Mbit/s)"
                    elif min_speed_value >= lower_warning_limit:
                        id_data["THRESHOLD MESSAGE (MIN)"] = f"MIN SPEED for ID {id_value} crosses Lower Warning Limit({lower_warning_limit} Mbit/s)"
                else:
                    id_data["THRESHOLD MESSAGE (MIN)"] = f"not_set"

                # Get values for "Discards In (Speed)", "Discards Out (Speed)", "Errors In (Speed)", and "Errors Out (Speed)"
                

            else:
                id_data["THRESHOLD MESSAGE (MIN)"] = f"No non-NaN values found in 'Traffic Total (Speed)(RAW)' for ID {id_value}"

        except Exception as e:
            id_data["THRESHOLD MESSAGE (MIN)"] = f"Error processing CSV data for ID {id_value}: {e}"

        # Append ID data dictionary to the list
        data_list.append(id_data)

# Create DataFrame from data_list
df_output = pd.DataFrame(data_list)

# Iterate over each ID to get the device name
# Iterate over each ID to get the device name
# Iterate over each ID to get the device name




# Display output in the terminal
for data_dict in data_list:
    print(f"ID {data_dict['ID']}:")
    print('-' * (len(f"ID {data_dict['ID']}:")))
    print(f"MAX SPEED: {data_dict.get('MAX SPEED', '< 0.01')}")
   # print(f"MAX SPEED RAW: {data_dict.get('MAX SPEED RAW', '< 0.01')}")
   # print(f"MAX SPEED DATE TIME: {data_dict.get('MAX SPEED DATE TIME', '< 0.01')}")
   # print(f"THRESHOLD MESSAGE (MAX): {data_dict.get('THRESHOLD MESSAGE (MAX)', '< 0.01')}")
    print(f"MIN SPEED: {data_dict.get('MIN SPEED', '< 0.01')}")
   # print(f"MIN SPEED RAW: {data_dict.get('MIN SPEED RAW', '< 0.01')}")
   # print(f"MIN SPEED DATE TIME: {data_dict.get('MIN SPEED DATE TIME', '< 0.01')}")
   # print(f"THRESHOLD MESSAGE (MIN): {data_dict.get('THRESHOLD MESSAGE (MIN)', '< 0.01')}")
   # print(f"DISCARD IN UPPER ERROR LIMIT: {data_dict.get('DISCARD IN UPPER ERROR LIMIT', 'not_set')}")
   # print(f"DISCARD IN LOWER ERROR LIMIT: {data_dict.get('DISCARD IN LOWER ERROR LIMIT', 'not_set')}")
   # print(f"DISCARD IN UPPER WARNING LIMIT: {data_dict.get('DISCARD IN UPPER WARNING LIMIT', 'not_set')}")
   # print(f"DISCARD IN LOWER WARNING LIMIT: {data_dict.get('DISCARD IN LOWER WARNING LIMIT', 'not_set')}")
   # print(f"DISCARD OUT UPPER ERROR LIMIT: {data_dict.get('DISCARD OUT UPPER ERROR LIMIT', 'not_set')}")
   # print(f"DISCARD OUT LOWER ERROR LIMIT: {data_dict.get('DISCARD OUT LOWER ERROR LIMIT', 'not_set')}")
   # print(f"DISCARD OUT UPPER WARNING LIMIT: {data_dict.get('DISCARD OUT UPPER WARNING LIMIT', 'not_set')}")
   # print(f"DISCARD OUT LOWER WARNING LIMIT: {data_dict.get('DISCARD OUT LOWER WARNING LIMIT', 'not_set')}")
    print(f"ERROR IN UPPER ERROR LIMIT: {data_dict.get('ERROR IN UPPER ERROR LIMIT', 'not_set')}")
    print(f"ERROR IN LOWER ERROR LIMIT: {data_dict.get('ERROR IN LOWER ERROR LIMIT', 'not_set')}")
    print(f"ERROR IN UPPER WARNING LIMIT: {data_dict.get('ERROR IN UPPER WARNING LIMIT', 'not_set')}")
    print(f"ERROR IN LOWER WARNING LIMIT: {data_dict.get('ERROR IN LOWER WARNING LIMIT', 'not_set')}")
    print(f"ERROR OUT UPPER ERROR LIMIT: {data_dict.get('ERROR OUT UPPER ERROR LIMIT', 'not_set')}")
    print(f"ERROR OUT LOWER ERROR LIMIT: {data_dict.get('ERROR OUT LOWER ERROR LIMIT', 'not_set')}")
    print(f"ERROR OUT UPPER WARNING LIMIT: {data_dict.get('ERROR OUT UPPER WARNING LIMIT', 'not_set')}")
    print(f"ERROR OUT LOWER WARNING LIMIT: {data_dict.get('ERROR OUT LOWER WARNING LIMIT', 'not_set')}")
    print(f"TRAFFIC TOTAL UPPER ERROR LIMIT: {data_dict.get('TRAFFIC TOTAL UPPER ERROR LIMIT', 'not_set')}")
    print(f"TRAFFIC TOTAL LOWER ERROR LIMIT: {data_dict.get('TRAFFIC TOTAL LOWER ERROR LIMIT', 'not_set')}")
    print(f"TRAFFIC TOTAL UPPER WARNING LIMIT: {data_dict.get('TRAFFIC TOTAL UPPER WARNING LIMIT', 'not_set')}")
    print(f"TRAFFIC TOTAL LOWER WARNING LIMIT: {data_dict.get('TRAFFIC TOTAL LOWER WARNING LIMIT', 'not_set')}")
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
