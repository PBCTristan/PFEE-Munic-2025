import json
import csv

data = json.load(open(r'C:\Users\tanth\Downloads\basic_signals\generated_data\straight_9.json', 'r'))

writer = csv.writer(open('output.csv', 'w', newline=''))
writer.writerow(['x', 'y', 'z'])
    
for item in data['data']:
    x, y, z = item['pos']
    writer.writerow([x, y, z])