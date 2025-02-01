import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# filter using the seuil method
def filtered(dataframe, x_std, y_std, z_std, fuse_method) -> pd.DataFrame:
    
    dataframe['Time'] = range(1, len(dataframe) + 1)
    signal_x = dataframe['accel_x']
    signal_y = dataframe['accel_y']
    signal_z = dataframe['accel_z']

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
    copy = dataframe.copy()
    copy['accel_x'] = signal_filtered
    copy['accel_y'] = signal_filtered_y
    copy['accel_z'] = signal_filtered_z
    if (fuse_method == "mean"):
        fused_signal = (signal_filtered_x + signal_filtered_y + signal_filtered_z) / 3 #mean
        copy['filtered_accel'] = fused_signal
    elif (fuse_method == "norm"):
        fused_signal = np.sqrt(signal_filtered_x**2 + signal_filtered_y**2 + signal_filtered_z**2) #euclidian
        copy['filtered_accel'] = fused_signal
    return copy
   

def seuil_denoising(dataframe, x_std, y_std, z_std, fuse_method):
    #if len(sys.argv) > 8:
    #    print("Usage: python script.py <input_csv_path> mode x_std y_std z_std mean/euclidian/show/save")
    #else:
     
    new_dataframe = filtered(dataframe, x_std, y_std, z_std, fuse_method)
    print(f'Processed {dataframe} filter signal with seuil')
    return new_dataframe
