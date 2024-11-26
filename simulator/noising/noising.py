import pandas as pd
import json
import numpy as np
import math as m
import argparse
import os

def create_df(file_path):
    with open(file_path, 'r') as f:
        global data
        data = json.load(f)
    records = []
    for entry in data['data']:
        timestamp = entry.get('timestamp')
        speed = entry.get('speed')
        accel = entry.get('accel')  # assuming 'accel' is a list of x, y, z components
        records.append({
        "timestamp": timestamp,
        "speed": speed,
        "accel_x": accel[0],  # Acceleration x-component
        "accel_y": accel[1],  # Acceleration y-component
        "accel_z": accel[2]   # Acceleration z-component
    })
    # Create DataFrame
    df = pd.DataFrame(records)
    return df

def rotation_matrix_x(theta):
    return np.array([[1, 0, 0],
                     [0, np.cos(theta), -np.sin(theta)],
                     [0, np.sin(theta), np.cos(theta)]])

def rotation_matrix_y(phi):
    return np.array([[np.cos(phi), 0, np.sin(phi)],
                     [0, 1, 0],
                     [-np.sin(phi), 0, np.cos(phi)]])

def rotation_matrix_z(psi):
    return np.array([[np.cos(psi), -np.sin(psi), 0],
                     [np.sin(psi), np.cos(psi), 0],
                     [0, 0, 1]])

def rotate_data(df, theta, phi, psi):
    rotation_matrix = rotation_matrix_x(theta) @ rotation_matrix_y(phi) @ rotation_matrix_z(psi)
    df[['accel_x', 'accel_y', 'accel_z']] = df[['accel_x', 'accel_y', 'accel_z']].values @ rotation_matrix.T
    return df

def noising(df):
    df['accel_x'] = df['accel_x'].apply(lambda x: x + (0.2 + 0.2) * np.random.random_sample() - 0.2)
    df['accel_y'] = df['accel_y'].apply(lambda x: x + (.2 + .2) * np.random.random_sample() - .2 - 9.81)
    df['accel_z'] = df['accel_z'].apply(lambda x: x + (.2 + .2) * np.random.random_sample() - .2)
    # df = rotate_data(df, theta, phi, psi)
    return df

def main():
    parser = argparse.ArgumentParser(description="Noise and rotate a generated acceleration file.")
    parser.add_argument(
        'filepath',
        type=str,
        help='The path to the file to process'
    )
    
    args = parser.parse_args()
    file_wo_ext = args.filepath.split('/')[-1].split('.')[0]
    
    # Check if the filepath exists
    if not os.path.exists(args.filepath):
        print(f"Error: The file '{args.filepath}' does not exist.")
        return

    df = create_df(args.filepath)
    
    theta, phi, psi = (0 + 2 * m.pi) * np.random.random_sample((3,)) - 2 * m.pi
    noised = noising(df)
    df_rot = rotate_data(noised, theta, phi, psi)

    obj = {
        'iscrash': data['iscrash'],
        'data': [{
            'timestamp': x[0],
            'accel_x': x[2],
            'accel_y': x[3],
            'accel_z': x[4],
        } for x in df_rot.values]
    }

    with open(f'{file_wo_ext}_treated.json', "w") as f:
        json.dump(obj, f)

if __name__ == "__main__":
    main()