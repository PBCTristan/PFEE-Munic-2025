# Seuil.py
The file is used to denoise a signal in a csv file with the seuil method and the following formula: ``` np.mean(signal_x) + int(x_std) * np.std(signal_x) ```.

## Usage

```python script.py <input_csv_path> mode x_std y_std z_std mean/euclidian``` 

There are 3 modes in this file:
- Original to show the noised signal
- Filter to use the seuil method, you can add the std values for the 3 axys. If not, it is 2 by default
- Fused to fuse the 3 axys into one. There a 2 method to fuse. Using the euclidian norm or compute the mean of the 3 axys for each value.  