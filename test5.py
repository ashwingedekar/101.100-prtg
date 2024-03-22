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
    server_parameters = dict(line.strip().split("=") for line in file) # server_paramter naam ki dict crate hori hai

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
for ids in id_values:           
 api_endpoint_upper_warning = f'https://{server_address}/api/getobjectproperty.htm?subtype=channel&id={ids}&subid=-1&name=limitmaxwarning&show=nohtmlencode&username=Ashwin.Gedekar&passhash=1132296586'
 response = requests.get(api_endpoint_upper_warning)
 print(response)
 print(response.text)
 



 with open(tiger.xml, "w") as file:
  file.write(response.text)
