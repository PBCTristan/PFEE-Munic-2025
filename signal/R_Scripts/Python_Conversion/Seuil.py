import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
import numpy as np
import sys


#accel_data = pd.read_csv("/home/thibault/pfee-munic/signal/enzo_1.csv")
def original(input_data):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)
    signal_x = accel_data['x']
    #signal_x = signal_x.iloc[:100]
    #print(signal_x[signal_x.index<100])
    signal_y = accel_data['y']
    signal_z = accel_data['z']
    plt.figure(figsize=(10, 6))

    plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')
    plt.plot(accel_data['Time'], signal_y, color='red', label='Signal Y Original')
    plt.plot(accel_data['Time'], signal_z, color='green', label='Signal Z Original')

    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.title('Seuil')
    plt.legend()
    plt.grid(True)
    plt.show()

def filter(input_data, x_std, y_std, z_std):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)
    signal_x = accel_data['x']
    signal_y = accel_data['y']
    signal_z = accel_data['z']

    if (x_std != None and x_std != ""): 
        threshold = np.mean(signal_x) + int(x_std) * np.std(signal_x)
    else:
        threshold = np.mean(signal_x) + 2 * np.std(signal_x)
    signal_filtered = np.where(np.abs(signal_x) >= threshold, signal_x, 0)

    if (y_std != None and y_std != ""): 
        threshold = np.mean(signal_y) + int(y_std) * np.std(signal_y)
    else:
        threshold = np.mean(signal_y) + 2 * np.std(signal_y)
    signal_filtered_y = np.where(np.abs(signal_y) >= threshold, signal_y, 0)

    if (z_std != None and z_std != ""): 
        threshold = np.mean(signal_z) + int(z_std) * np.std(signal_z)
    else:
        threshold = np.mean(signal_z) + 2 * np.std(signal_z)
    signal_filtered_z = np.where(np.abs(signal_z) >= threshold, signal_z, 0)

    plt.figure(figsize=(10, 6))

    plt.plot(accel_data['Time'], signal_filtered, color='blue', label='Signal X filtré')
    plt.plot(accel_data['Time'], signal_filtered_y, color='red', label='Signal Y filtré')
    plt.plot(accel_data['Time'], signal_filtered_z, color='green', label='Signal Z filtré')

    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.title('Seuil')
    plt.legend()
    plt.grid(True)
    plt.show()

def fused(input_data, x_std, y_std, z_std, fuse_method):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)
    signal_x = accel_data['x']
    signal_y = accel_data['y']
    signal_z = accel_data['z']

    if (x_std != None and x_std != ""): 
        threshold = np.mean(signal_x) + int(x_std) * np.std(signal_x)
    else:
        threshold = np.mean(signal_x) + 2 * np.std(signal_x)
    signal_filtered = np.where(np.abs(signal_x) >= threshold, signal_x, 0)

    if (y_std != None and y_std != ""): 
        threshold = np.mean(signal_y) + int(y_std) * np.std(signal_y)
    else:
        threshold = np.mean(signal_y) + 2 * np.std(signal_y)
    signal_filtered_y = np.where(np.abs(signal_y) >= threshold, signal_y, 0)

    if (z_std != None and z_std != ""): 
        threshold = np.mean(signal_z) + int(z_std) * np.std(signal_z)
    else:
        threshold = np.mean(signal_z) + 2 * np.std(signal_z)
    signal_filtered_z = np.where(np.abs(signal_z) >= threshold, signal_z, 0)

    plt.figure(figsize=(10, 6))
    if (fuse_method == "mean"):
        fused_signal = (signal_filtered + signal_filtered_y + signal_filtered_z) / 3 #mean
    else:
        fused_signal = np.sqrt(signal_filtered**2 + signal_filtered_y**2 + signal_filtered_z**2) #euclidian
        

    plt.plot(accel_data['Time'], fused_signal, label='Fused Signal (Magnitude)', color='purple')
    plt.xlabel('Time')
    plt.ylabel('Fused value')
    plt.title('Fused value (X, Y, Z)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 8:
        print("Usage: python script.py <input_csv_path> mode x_std y_std z_std mean/euclidian")
    else:
        input_csv_path = sys.argv[1]
        mode = sys.argv[2]
        match mode:
            case "original":
                original(input_csv_path)
                print(f'Processed {input_csv_path} original signal')
            case "fused":
                x_std = sys.argv[3]
                y_std = sys.argv[4]
                z_std = sys.argv[5]
                fuse_method = sys.argv[6]
                fused(input_csv_path, x_std, y_std, z_std, fuse_method)
                print(f'Processed {input_csv_path} fused signal')
            case "filter":
                x_std = sys.argv[3]
                y_std = sys.argv[4]
                z_std = sys.argv[5]
                
                filter(input_csv_path, x_std, y_std, z_std)
                print(f'Processed {input_csv_path} filter signal')