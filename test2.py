import csv
import xml.etree.ElementTree as ET

tree = ET.parse('example.xml')
root = tree.getroot()

data = []

for device in root.findall('.//device'):
    device_id = device.find('id').text
    device_name = device.find('name').text

    for sensor in device.findall('.//sensor'):
        sensor_id = sensor.find('id').text
        sensor_type = sensor.find('sensortype').text
        sensor_name = sensor.find('name').text

        data.append([device_name, device_id, sensor_name, sensor_id,sensor_type])

with open('101.100_DST.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Device Name', 'Device ID', 'Sensor Name', 'Sensor ID', 'Sensor Type'])
    csv_writer.writerows(data)
