import pandas as pd
from simulator.noising import noising as cctn
from signal_processing import Denoising as dn, calibration as cali
from simulator.scripts import run as simu
import argparse
import json
import os

def GetDataframeFromFile(data):
# Check if the filepath exists
    records = []
    for entry in data['data']:
        timestamp = entry.get('timestamp')
        speed = entry.get('speed')
        records.append({
        "timestamp": timestamp,
        "accel_x": entry.get('accel_x'),  # Acceleration x-component
        "accel_y": entry.get('accel_y'),  # Acceleration y-component
        "accel_z": entry.get('accel_z')   # Acceleration z-component
    })
    # Create DataFrame
    df = pd.DataFrame(records)
    return df

def json_to_object(data, cls: type[any]) -> object:
    try:
        # Create an object instance from the JSON data
        # Assumes the keys in JSON match the attributes of the class
        if data != None:
            obj = cls(**data)
            return obj
        return None
    except TypeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in json_to_object: {e}")

class SimuConfig():
    def __init__(self, env:str="donkey-generated-track-v0", number:list[int] = [1,1,1,1], frames:int = 100, logfile:str|None = None, autolog:bool = True):
        self.env:str = env
        self.number:list[int] = number
        self.frames:int = frames
        self.logfile:str|None = logfile
        self.autolog:bool = autolog
        self.noise:bool = False
    
    def launchSimu(self, raw_data_path):
        directory_path = os.path.dirname(__file__)
        simu.runSimu(args=self, program_directory_path = directory_path, raw_data_path = raw_data_path)


class NoisingConfig():
    def __init__(self):
        self.config: str = ""


class DenoisingConfig():
    def __init__(self,algo_method:str = "seuil", mode:str = "filter", x:int = 2, y:int = 2, z:int = 2, cutoff:float = 0.1, method:str = "save"):
        self.algo_method = algo_method
        self.mode = mode
        self.x = x
        self.y = y
        self.z = z
        self.cutoff = cutoff
        self.method = method
    
    def denoising(self, dataframe) -> (pd.DataFrame | None):
        return dn.denoising(algo_method=self.algo_method,
                     dataframe=dataframe,
                     mode=self.mode,
                     x=self.x,
                     y=self.y,
                     z=self.z,
                     cutoff=self.cutoff,
                     method=self.method)

class CalibrationConfig():
    def __init__(self):
        self.config: str = ""

class MLConfig():
    def __init__(self):
        self.config: str = ""

class optionChooser():
    def __init__(self):
        # simulation subObject
        self.simulateur: SimuConfig|None = None
        self.raw_data_path: str|None = None

        # Noising subObject
        self.Noising: NoisingConfig|None = None
        self.Noised_data_path: str|None = None

        # DeNoising subObject
        self.DeNoising: DenoisingConfig|None = None
        self.DeNoised_data_path: str|None = None

        # Calibration subObject
        self.calibration: CalibrationConfig|None = None
        self.calibrated_data_path: str|None = None

        # ML subObject
        self.ml: MLConfig|None = None

    @staticmethod
    def FromJson(json: object) -> 'optionChooser':
        print(json)
        ret = optionChooser()
        ret.simulateur = json_to_object(json["simulateur"], SimuConfig)
        ret.raw_data_path = json["raw_data_path"]
        ret.Noising = json_to_object(json["Noising"], NoisingConfig)
        ret.Noised_data_path = json["Noised_data_path"]
        ret.DeNoising = json_to_object(json["DeNoising"], DenoisingConfig)
        ret.DeNoised_data_path = json["DeNoised_data_path"]
        ret.calibration = json_to_object(json["calibration"], CalibrationConfig)
        ret.calibrated_data_path = json["calibrated_data_path"]
        ret.ml = json_to_object(json["ml"], CalibrationConfig)
        return ret
    
    def execSimu(self):
        self.simulateur.launchSimu(self.raw_data_path)
        

    def execNoising(self):
        # think of ways to improve convertion by using the config file 
        try:
            # Get a list of all files and directories in the specified path
            all_items = os.listdir(self.raw_data_path)
            
            # Filter out directories, keeping only files
            files = [(os.path.join(self.raw_data_path, item), os.path.join(self.Noised_data_path, item)) for item in all_items if os.path.isfile(os.path.join(self.raw_data_path, item))]
            
            for source_path, target_path in files:
                cctn.convert_clean_to_noised(source_path, target_path)
        except FileNotFoundError:
            print(f"Error: The directory '{self.raw_data_path}' does not exist.")
        except Exception as e:
            print(f"An unexpected error occurred in execNoising: {e}")


    def execDenoising(self):
        try:
            # Get a list of all files and directories in the specified path
            all_items = os.listdir(self.Noised_data_path)
            
            # Filter out directories, keeping only files
            files = [(os.path.join(self.Noised_data_path, item), os.path.join(self.DeNoised_data_path, item)) for item in all_items if os.path.isfile(os.path.join(self.Noised_data_path, item))]
            
            for source_path, target_path in files:
                with open(source_path, 'r') as f:
                    data = json.load(f)
                df = GetDataframeFromFile(data)
                denoisedDF = self.DeNoising.denoising(df)
                obj = {
                    'iscrash': data['iscrash'],
                    'data': [{
                        'timestamp': x[0],
                        'accel_x': x[2],
                        'accel_y': x[3],
                        'accel_z': x[4],
                    } for x in denoisedDF.values]
                }
                with open(target_path, "w") as f:
                    json.dump(obj, f)

        except FileNotFoundError:
            print(f"Error: The directory '{self.Noised_data_path}' does not exist.")
        # except Exception as e:
        #     print(f"An unexpected error occurred in execDenoising: {e}")


    def execCalibration(self):
        try:
            # Get a list of all files and directories in the specified path
            all_items = os.listdir(self.DeNoised_data_path)
            
            # Filter out directories, keeping only files
            files = [(os.path.join(self.DeNoised_data_path, item), os.path.join(self.calibrated_data_path, item)) for item in all_items if os.path.isfile(os.path.join(self.DeNoised_data_path, item))]
            
            for source_path, target_path in files:
                with open(source_path, 'r') as f:
                    data = json.load(f)
                df = GetDataframeFromFile(data)
                (calibratedDF, _) = cali.calibrate(df)
                obj = {
                    'iscrash': data['iscrash'],
                    'data': [{
                        'timestamp': x[0],
                        'accel_x': x[2],
                        'accel_y': x[3],
                        'accel_z': x[4],
                    } for x in calibratedDF.values]
                }
                with open(target_path, "w") as f:
                    json.dump(obj, f)

        except FileNotFoundError:
            print(f"Error: The directory '{self.raw_data_path}' does not exist.")
        # except Exception as e:
        #     print(f"An unexpected error occurred in execCalibration: {e}")
    
    def execML(self):
        try:
            # Get a list of all files and directories in the specified path
            all_items = os.listdir(self.calibrated_data_path)
            
            # Filter out directories, keeping only files
            files = [os.path.join(self.raw_data_path, item) for item in all_items if os.path.isfile(os.path.join(self.raw_data_path, item))]
            
            for source_path in files:
                print("gnii")
        except FileNotFoundError:
            print(f"Error: The directory '{self.raw_data_path}' does not exist.")
        # except Exception as e:
        #     print(f"An unexpected error occurred in execML: {e}")

    def execPipeline(self):

        # Simulation execution
        if self.simulateur != None:
            self.execSimu()

        # Noising execution
        if self.Noising != None:
            self.execNoising()
            
        # Denoising execution
        if self.DeNoising != None:
            self.execDenoising()

        # Calibration execution
        if self.calibration != None:
            self.execCalibration()

        # ML execution
        if self.ml != None:
            self.execML()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Allow for a config file to be loaded to process data.")
    parser.add_argument(
        "-f",
        '--filepath',
        type=str,
        required=True,
        help='The path to the json config file to process'
    )
    args = parser.parse_args()
    opt = optionChooser()
    # Check if the filepath exists
    if not os.path.exists(args.filepath):
        print(f"Error: The file '{args.filepath}' does not exist.")
    else:
        with open(args.filepath, 'r') as f:
            opt = optionChooser.FromJson(json.load(f))
    
    opt.execPipeline()

