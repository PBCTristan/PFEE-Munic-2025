import numpy as np

class Record:
  def __init__(self):
    self.is_crash = False
    self.datas = []
    self.actions = []

  def add_data(self, data, action):
    self.datas.append(data)
    self.actions.append(action)

  def to_json(self):
    return {
      'iscrash': self.is_crash,
      'data': self.datas,
      'actions': self.actions
    }
  