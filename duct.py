# Initialize an empty dictionary to store key-value pairs
server_parameters = {}

# Open the file "server_address.txt" in read mode
with open("server_address.txt", "r") as file:
    
    # Iterate over each line in the file
    for line in file:
        
        # Remove leading and trailing whitespace from the line
        line = line.strip()
        
        # Split the line into key and value using the "=" character as separator
        key, value = line.split("=")
        
        # Add the key-value pair to the server_parameters dictionary
        server_parameters[key] = value
