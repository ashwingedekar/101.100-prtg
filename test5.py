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
user_name = server_parameters.get("username")
pass_hash = server_parameters.get("passhash")
# Read flags from the "min_max_flags.txt" file

# Initialize an empty dictionary to store the key-value pairs
data_dict = {}

# Open the file containing the key-value pairs
file_path = 'min_max_flags.txt'  # Specify the path to your file
with open(file_path, 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Split each line by '=' to separate key and value
        parts = line.strip().split('=')
        # Check if the line is properly formatted with key and value
        if len(parts) == 2:
            key, value = parts
            # Add the key-value pair to the dictionary
            data_dict[key.strip()] = value.strip()

# Print the dictionary to verify


# Sirf values ko extract karne ke liye
values = list(data_dict.values())

# Ab aap ye values ko API mein pass kar sakte hain
#print(values)  # Example mein print kiya hai





# Construct API endpoints for upper and lower error and warning limits for all IDs
api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?id={value}&subtype=channel&subid=-1&name=limitmaxwarning&show=nohtmlencode&username={user_name}&passhash={pass_hash}'

response = requests.get(api_endpoint_upper_warning)

print(response)

abc = response.text

print(abc)
#/api/getobjectproperty.htm?id=1003&subtype=channel&subid=0&name=limitmaxwarning&show=nohtmlencode



# Create dictionaries to store upper and lower error and warning limits for each ID
#upper_warning_limits = {}

#https://tp-prtg-101-100.comtelindia.com:10443/api/getobjectproperty.htm?id=10705&subtype=channel&subid=12&name=limitmaxerror&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586

