import pandas as pd
import numpy as np
import sys

def round_to_precision(value, precision):
    return np.round(value / precision) * precision

def process_csv(input_path, output_path, precision=0.6276256):
    df = pd.read_csv(input_path)

    df['x'] = df['x'].apply(lambda v: round_to_precision(v, precision))
    df['y'] = df['y'].apply(lambda v: round_to_precision(v, precision))
    df['z'] = df['z'].apply(lambda v: round_to_precision(v, precision)) 

    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_csv_path> <output_csv_path>")
    else:
        input_csv_path = sys.argv[1]
        output_csv_path = sys.argv[2]
        process_csv(input_csv_path, output_csv_path)