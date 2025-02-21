# Usage

This directory contains the 5 available methods to denoise a signal. In the pipeline, this step takes place after the calibration and rotation of the axys. The files are used in the denoising.py file with the selected method. Here is the algorithm for each:

# Seuil.py
The file is used to denoise a signal in a Dataframe with the seuil method and the following formula: ``` np.mean(signal_x) + int(x_std) * np.std(signal_x) ```. For each value, if an axys value is less than the threshold then it is set to 0. The default value of x_std, y_std and z_std are 2. To use this method in denoising.py we call the function seuil_denoising()

# auto\_corr.py
The file is used to denoise a signal in a Dataframe using a model that check its own signal at different intervals. There are no value to pass as arguments. To use this method in denoising.py we call the function auto_corr_denoising()

# cross\_axys.py
The file is used to denoise a signal in a Dataframe using a model that denoise an axys using the correlation with the 
2 others. The target is the axys to denoise and we fit the 2 others.

# fourrier.py
The file is used to denoise a signal in a Dataframe using fourrier. First, frequencies outside a range defined by a "cutoff" threshold are removed by setting them to zero. Then, the inverse Fourier transform is applied to reconstruct the signal with the filtered frequencies. The default value of the cutoff is 0.1.

# square.py
The final method is fitting a signal to a polynomial model using the mean square error. The default value of x_degree, y_degree and z_degree are 2 like in the seuil method.
