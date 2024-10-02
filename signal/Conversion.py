import json
import csv

data = json.load(open(r'C:\Users\Gérard Grokoum\Downloads\garice_tiens.json', 'r'))

writer = csv.writer(open('outpute.csv', 'w', newline=''))
writer.writerow(['x', 'y', 'z'])
    
for item in data['data']:
    x, y, z = item['accel']
    writer.writerow([x, y, z])