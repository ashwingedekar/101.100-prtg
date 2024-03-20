data_dict = {}

# Open the file containing the key-value pairs
file_path = 'your_file.txt'  # Specify the path to your file
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
print(data_dict)
