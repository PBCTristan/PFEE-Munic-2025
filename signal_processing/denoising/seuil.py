import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# filter using the seuil method
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

    return signal_filtered, signal_filtered_y, signal_filtered_z

# To fuse all 3 axys into one using norm or mean
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

def seuil_denoising(input_csv_path, mode, x_std, y_std, z_std, method):
    #if len(sys.argv) > 8:
    #    print("Usage: python script.py <input_csv_path> mode x_std y_std z_std mean/euclidian/show/save")
    #else:
        match mode:
            case "fused":
                fused(input_csv_path, x_std, y_std, z_std, method)
                print(f'Processed {input_csv_path} fused signal with seuil')
            case _:
                x_result, y_result, z_result = filter(input_csv_path, x_std, y_std, z_std)
                print(f'Processed {input_csv_path} filter signal with seuil')
                return x_result, y_result, z_result