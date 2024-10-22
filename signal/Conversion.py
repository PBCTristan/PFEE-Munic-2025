import json
import csv

data = json.load(open(r'/home/thibault/pfee-munic/gary3.json', 'r'))

writer = csv.writer(open('outpute.csv', 'w', newline=''))
writer.writerow(['x', 'y', 'z'])


sum_x = 0
sum_y = 0
sum_z = 0

count = 0
for item in data['data']:
    x, y, z = item['accel']
    sum_x += x
    sum_y += y
    sum_z += z
    count += 1

sum_x /= count
sum_y /= count
sum_y /= count
print(sum_x)
print(sum_y)
print(sum_z)
for item in data['data']:
    x, y, z = item['accel']
    if (x != None and y != None and z != None):
    	writer.writerow([x - sum_x, y - sum_y, z - sum_z])

