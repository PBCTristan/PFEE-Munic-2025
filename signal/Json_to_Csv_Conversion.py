import json
import csv

import pandas as pd
import numpy as np
import sys


def convert(input_filename, output_filename, noising):
    with open(input_filename, 'r') as json_file:
        data = json.load(json_file)
    
    with open(output_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['x', 'y', 'z'])
        
        for item in data['data']:
            if noising == "True" or noising == "true":
                noise = (0.1 + 0.5) * np.random.random_sample((3,)) - 0.6
                x, y, z = item['accel'] + noise
            else:
                x, y, z = item['accel']
            writer.writerow([x, y, z])
    print(f'Processed {input_filename} and saved to {output_filename}')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_csv_path> <output_csv_path> true/false")
    else:
        input_csv_path = sys.argv[1]
        output_csv_path = sys.argv[2]
        noising = sys.argv[3]
        convert(input_csv_path, output_csv_path, noising)
