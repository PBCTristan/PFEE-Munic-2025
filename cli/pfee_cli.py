from load_data_dir import dataDir

opening_string = """welcome to the pfee cli pipeline
choose amoug the folowing option by typing the corresponding number"""
menuString =  """---------------------------------------
[1] print hello world
[2] exit cli
[3] set dir for data"""

class optionChooser():
    def __init__(self):
        self.path_to_data = None
        self.noise_Algo = None
        self.denoise_Algo = None


    def printInfo(self):
        print("---------------------------------------")
        print(f"path to data: {self.path_to_data}")
        print(f"noising algorithm: {self.noise_Algo}")
        print(f"unnoising algorithm: {self.denoise_Algo}")


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
