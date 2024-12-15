from denoising.seuil import seuil_denoising
from denoising.original import original
from denoising.square import square_denoising
from denoising.auto_corr import auto_corr_denoising
from denoising.cross_axys import cross_axys_denoising
from denoising.fourrier import fourrier_denoising
from denoising.saving import saving
def denoising(algo_method="seuil", input="test.csv", mode="filter", x=2, y=2, z=2, cutoff=0.1, method="save"):
    match algo_method:
        case "autocorr":
            x_filtered, y_filtered, z_filtered = auto_corr_denoising(input)
        case "fourrier":
            x_filtered, y_filtered, z_filtered = fourrier_denoising(input, cutoff)
        case "cross-axys":
            x_filtered, y_filtered, z_filtered = cross_axys_denoising(input)
        case "square":
            x_filtered, y_filtered, z_filtered = square_denoising(input, x, y, z)
        case "original":
            original(input)
            return
        #default case is seuil
        case _:
            x_filtered, y_filtered, z_filtered = seuil_denoising(input, mode, x, y, z, method)

    saving(input, algo_method, method, x_filtered, y_filtered, z_filtered)

#denoising(algo_method="seuil", input="gary.csv", method="shows")