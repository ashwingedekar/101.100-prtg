import csv
import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('example.xml')
root = tree.getroot()

# Create a list to store extracted data
data = []

# Iterate over all device elements
for device in root.findall('.//device'):
    device_id = device.find('id').text
    device_name = device.find('name').text
    
    # Iterate over all sensor elements within the device
    for sensor in device.findall('.//sensor'):
        sensor_id = sensor.find('id').text
        sensor_name = sensor.find('name').text
        
        # Append data to the list
        data.append([device_name, device_id, sensor_name, sensor_id])

# Write data to CSV file
with open('output.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write header row
    csv_writer.writerow(['Device Name', 'Device ID', 'Sensor Name', 'Sensor ID'])
    
    # Write data rows
    csv_writer.writerows(data)

print("CSV file saved successfully.")
