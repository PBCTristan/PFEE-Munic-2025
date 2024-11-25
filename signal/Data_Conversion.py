import json
import csv

data = json.load(open(r'/home/thibault/pfee-munic/enzo_4.json', 'r'))

writer = csv.writer(open('enzo_4.csv', 'w', newline=''))
writer.writerow(['x', 'y', 'z'])


sum_x = 0
sum_y = 0
sum_z = 0

count = 0
for item in data:
    x = float(item['x'])
    y = float(item['y'])
    z = float(item['z'])
    sum_x += x
    sum_y += y
    sum_z += z
    count += 1

sum_x /= count
sum_y /= count
sum_z /= count
print(sum_x)
print(sum_y)
print(sum_z)
for item in data:
    x = float(item['x'])
    y = float(item['y'])
    z = float(item['z'])
    if (x != None and y != None and z != None):
        writer.writerow([x - sum_x, y - sum_y, z - sum_z])
