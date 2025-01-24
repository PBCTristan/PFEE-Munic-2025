from signal_processing.denoising.seuil import seuil_denoising
from signal_processing.denoising.original import original
from signal_processing.denoising.square import square_denoising
# from signal_processing.denoising.auto_corr import auto_corr_denoising
from signal_processing.denoising.cross_axys import cross_axys_denoising
from signal_processing.denoising.fourrier import fourrier_denoising
from signal_processing.denoising.saving import saving
def denoising(algo_method="seuil", dataframe=None, mode="filter", x=2, y=2, z=2, cutoff=0.1, method="save"):
    match algo_method:
        # case "autocorr":
        #     return auto_corr_denoising(dataframe)
        case "fourrier":
            return fourrier_denoising(dataframe, cutoff)
        case "cross-axys":
            return cross_axys_denoising(dataframe)
        case "square":
            return square_denoising(dataframe, x, y, z)
        case "original":
            original(dataframe)
            return
        #default case is seuil
        case _:
            return seuil_denoising(dataframe, mode, x, y, z, method)

    #saving(input, algo_method, method, x_filtered, y_filtered, z_filtered)

#denoising(algo_method="seuil", input="gary.csv", method="shows")