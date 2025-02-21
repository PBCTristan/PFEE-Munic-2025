## Usage

The recommanded way to test the denoising algorithms is to use the denoising.py and select the desired method. The default one is the Seuil method. In the pipeline, this step takes a panda Dataframe as an argument and the parameters of your method and gives another denoised panda Dataframe.

```denoising(algo_method, dataframe, mode, x, y, z, cutoff, method)```

Here are the arguments values:

algo_method is the algorithm to denoise the signal. There are 5 methods, AutoCorr, Cross-axys, Fourrier, Seuil, Square. Seuil is the default one, for more explanation you can check the README in the denoising directory.

dataframe is the signal passed in the pipeline. It contains 3 columns for each axys, accel_x, accel_y and accel_z.

For mode, there are 3 modes for each algorithm:
- "filter" to keep the 3 axys
- "mean" to fuse the denoised axys using the mean for each value.
- "norm" to fuse the denoised axys using the norm method : sqrt(x^2 + y^2 + z^2)

x, y and z are used in the seuil and square methods, the default values are 2.

cutoff is used in the fourrier method, the default value is 0,1.

For method, there are 3 methods in this file:
- "show" to show the denoised signal.
- "save" to save the denoised signal in a csv file.
- "skip" to pass directly the dataframe to the next step of the pipeline.
