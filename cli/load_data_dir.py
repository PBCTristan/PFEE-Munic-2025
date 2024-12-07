import os


class dataDir(): 
    
    def askForInput(self, opt) -> str | None:
        need_input = True
        extstr = None
        while need_input:
            dataDirStr = """Give a path to the directory containing all the data you want to use
nothing if you want to exit"""
            print(dataDirStr)
            if (opt.path_to_data):
                print(f"actual chosen path:\n{opt.path_to_data}")
            command = input(">> ")
            if (command != ""):
                if (os.path.exists(command)):
                    extstr = command
                    need_input = False
                else:
                    print("This path does not exist")
            else:
                need_input = False

        return extstr