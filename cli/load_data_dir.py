import os


class dataDir(): 
    
    def askForInput(self, path) -> str | None:
        need_input = True
        extstr = None
        while need_input:
            dataDirStr = """Give a valid directory path
nothing if you want to exit"""
            print(dataDirStr)
            if (path):
                print(f"actual chosen path:\n{path}")
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