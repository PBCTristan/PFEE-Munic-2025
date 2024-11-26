import json
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os

def create_df(file_path):
    with open(file_path, 'r') as f:
        global data
        data = json.load(f)
    records = []
    for entry in data['data']:
        timestamp = entry.get('timestamp') # assuming 'accel' is a list of x, y, z components
        records.append({
        "timestamp": timestamp,
        "accel_x": entry.get('accel_x'),  # Acceleration x-component
        "accel_y": entry.get('accel_y'),  # Acceleration y-component
        "accel_z": entry.get('accel_z')   # Acceleration z-component
    })
    # Create DataFrame
    df = pd.DataFrame(records)
    return df

def main():
    parser = argparse.ArgumentParser(description="Noise and rotate a generated acceleration file.")
    parser.add_argument(
        'filepath',
        type=str,
        help='The path to the file to process'
    )
    
    args = parser.parse_args()
    df = create_df(args.filepath)
    plt.plot(df['timestamp'],df['accel_x'], 'b', label='Acceleration on x axis')
    plt.plot(df['timestamp'],df['accel_y'], 'g', label='Acceleration on y axis')
    plt.plot(df['timestamp'],df['accel_z'], 'r', label='Acceleration on z axis')
    plt.xlabel('Timestamp')
    plt.ylabel('Acceleration')
    plt.legend(loc='upper left', draggable=True)
    plt.title(f'{os.path.basename(args.filepath)}')
    plt.show()

if __name__ == "__main__":
    main()