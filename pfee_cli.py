from cli.load_data_dir import dataDir
from simulator.noising import noising as cctn
import argparse
import json
import os

opening_string = """welcome to the pfee cli pipeline
choose among the folowing options by typing the corresponding number"""
menuString =  """---------------------------------------
[1] print hello world
[2] exit cli
[3] set dir for un-noised data
[4] change if data is to be noised or not
[5] set dir for noised data
[6] set denoising algo
[7] set dir for cleaned data"""

class optionChooser():
    def __init__(self, path_to_data = None, should_noise = False, path_to_noised_data = None,
                 denoise_Algo = None, path_to_traited_data = None):
        self.path_to_data = path_to_data
        self.should_noise = should_noise
        self.path_to_noised_data = path_to_noised_data
        self.denoise_Algo = denoise_Algo
        self.path_to_traited_data = path_to_traited_data

    @staticmethod
    def FromJson(json: object) -> 'optionChooser':
        print(json)
        return optionChooser(json["path_to_data"], json["should_noise"], json["path_to_noised_data"],
                             json["denoise_Algo"], json["path_to_traited_data"])

    def printInfo(self):
        print("---------------------------------------")
        print(f"path to data: {self.path_to_data}")
        print(f"should noise data: {self.should_noise}")
        print(f"path to noised data: {self.path_to_noised_data}")
        print(f"choosen denoising algorithm : {self.denoise_Algo}")
        print(f"path to traited data: {self.path_to_traited_data}")

    def execPipeline(self):
        if (self.should_noise and self.path_to_data and self.path_to_noised_data):
            cctn.noising(self.path_to_data , self.path_to_noised_data)
        

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
                    path_data = dirmenu.askForInput(opt.path_to_data)
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
                    path_data = dirmenu.askForInput(opt.path_to_noised_data)
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
                    path_data = dirmenu.askForInput(opt.path_to_traited_data)
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




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Allow for a config file to be loaded to process data.")
    parser.add_argument(
        "-f",
        '--filepath',
        type=str,
        help='The path to the json file to process'
    )
    args = parser.parse_args()
    opt = optionChooser()
    # Check if the filepath exists
    if not os.path.exists(args.filepath):
        print(f"Error: The file '{args.filepath}' does not exist.")
    else:
        with open(args.filepath, 'r') as f:
            opt = optionChooser.FromJson(json.load(f))
    
    runLoop = True
    
    print(opening_string)

    while runLoop:
        opt.printInfo()
        print(menuString)
        command = input(">> ")
        runLoop = menuSwitch(command, opt)
