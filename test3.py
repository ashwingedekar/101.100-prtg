import csv
import xml.etree.ElementTree as ET

tree = ET.parse('abc.xml')
root = tree.getroot()

data = []

for book in root.findall('.//book'):
   book_name = book.find('title').text
   book_author = book.find('author').text

   data.append([book_name, book_author])

with open('pihu.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Book Name','Author'])
    csv_writer.writerows(data)

