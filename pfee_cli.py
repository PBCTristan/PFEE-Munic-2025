from cli.load_data_dir import dataDir
from simulator.noising import noising as cctn

opening_string = """welcome to the pfee cli pipeline
choose amoug the folowing option by typing the corresponding number"""
menuString =  """---------------------------------------
[1] print hello world
[2] exit cli
[3] set dir for un-noised data
[4] change if data is to be noised or not
[5] set dir for noised data
[6] set denoising algo
[7] set dir for cleaned data"""

class optionChooser():
    def __init__(self):
        self.path_to_data = None
        self.should_noise = False
        self.path_to_noised_data = None
        self.denoise_Algo = None
        self.path_to_traited_data = None


    def printInfo(self):
        print("---------------------------------------")
        print(f"path to data: {self.path_to_data}")
        print(f"should noise data: {self.should_noise}")
        print(f"path to noised data: {self.path_to_noised_data}")
        print(f"choosen denoising algorithm : {self.denoise_Algo}")
        print(f"path to traited data: {self.path_to_traited_data}")


def menuSwitch(input: str, opt: optionChooser) -> bool:
    try:
        optionNum = int( input, base=10)
        match (optionNum):
            case 1:
                print("hello world")
                return True
            case 2:
                print("closing cli")
                return False
            case 3:
                dirmenu = dataDir()
                try:
                    path_data = dirmenu.askForInput(opt)
                    opt.path_to_data = path_data if path_data else opt.path_to_data
                except Exception as e:
                    print(e)
                finally:
                    return True
            case 4:
                print("add behavior to change between True and False")
                return True
            case 5:
                dirmenu = dataDir()
                try:
                    path_data = dirmenu.askForInput(opt)
                    opt.path_to_noised_data = path_data if path_data else opt.path_to_noised_data
                except Exception as e:
                    print(e)
                finally:
                    return True
            case 4:
                print("add behavior to change for different noising algo")
                return True
            case 7:
                dirmenu = dataDir()
                try:
                    path_data = dirmenu.askForInput(opt)
                    opt.path_to_traited_data = path_data if path_data else opt.path_to_traited_data
                except Exception as e:
                    print(e)
                finally:
                    return True
            case _:
                print("wtf")

    except:
        print("invalid input format, must be a non-floating number")
        return True



runLoop = True
opt = optionChooser()
print(opening_string)

while runLoop:
    opt.printInfo()
    print(menuString)
    command = input(">> ")
    runLoop = menuSwitch(command, opt)
