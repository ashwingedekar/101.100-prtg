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
user = server_parameters.get("username")
passe = server_parameters.get("passhash")


id_values = []




progress_bar = tqdm(total=len(id_values), desc="Fetching limits for each ID")

# Make the API requests for each ID to get the limits
for id_value in id_values:
    id_data = {}
    

    device_name_endpoint = f'https://{server_address}/api/getsensordetails.json?id={id_value}&username={user}&passhash={passe}'
    device_name_response = requests.get(device_name_endpoint)
    if device_name_response.status_code == 200:
        device_name_json = device_name_response.json()
        parent_device_name = device_name_json["sensordata"]["parentdevicename"]
        id_data["Device Name"] = parent_device_name
    else:
        id_data["Device Name"] = "Device name not available"

    
    
    
    # Update the progress bar
    progress_bar.update(1)


# Close the progress bar
progress_bar.close()

#

# Create the output directory if it doesn't exist
output_directory = "output"
os.makedirs(output_directory, exist_ok=True)

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Construct the full file path for the output file
output_file_path = os.path.join(output_directory, f"id_and_name_{current_datetime}.csv")

# Write the DataFrame to CSV file
df_output.to_csv(output_file_path, index=False)

# Print the output file path to the terminal
print(f"\nOutput has been saved to {output_file_path}")
