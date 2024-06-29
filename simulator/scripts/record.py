class Record:
  def __init__(self, type):
    self.is_crash = False
    self.type = type
    self.datas = []
    self.actions = []

  def add_data(self, data, action):
    self.datas.append(data)
    self.actions.append(action)

  def to_json(self):
    return {
      'iscrash': self.is_crash,
      'type': self.type,
      'data': self.datas,
      'actions': self.actions
    }
  