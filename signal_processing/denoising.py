from denoising.seuil import seuil_denoising
from denoising.original import original
from denoising.square import square_denoising
from denoising.auto_corr import auto_corr_denoising
from denoising.cross_axys import cross_axys_denoising
from denoising.fourrier import fourrier_denoising
from denoising.saving import saving
def denoising(algo_method="seuil", dataframe=None, mode="filter", x=2, y=2, z=2, cutoff=0.1, method="skip"):
    if (method == "save" or method == "show")
        saving(method, dataframe)
    match algo_method:
        case "autocorr":
            return auto_corr_denoising(dataframe, mode)
        case "fourrier":
            return fourrier_denoising(dataframe, cutoff, mode)
        case "cross-axys":
            return cross_axys_denoising(dataframe, mode)
        case "square":
            return square_denoising(dataframe, x, y, z, mode)
        case "original":
            original(dataframe)
            return
        #default case is seuil
        case _:
            return seuil_denoising(dataframe, x, y, z, mode)


#denoising(algo_method="seuil", input="gary.csv", method="shows")
