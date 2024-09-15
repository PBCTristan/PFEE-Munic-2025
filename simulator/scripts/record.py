class Record:
    def __init__(self, type):
        self.is_crash = False
        self.type = type
        self.datas = []

    def add_data(self, data):
        self.datas.append(data)
        if data["hit"] != "none":
            self.is_crash = True

    def to_json(self):
        return {
            "iscrash": self.is_crash,
            "type": self.type,
            "data": self.datas,
        }
