from common import Const
import json


class Task(object):
    def __init__(self, name, sx, sy):
        self.name = name
        self.sx, self.sy = sx, sy
        with open("./data/dst/{}.json".format(self.name)) as f:
            self.pa = json.loads(f.read())
        self.data = self.pa["data"]
        self.cols = self.pa["cols"]
        self.rows = self.pa["rows"]
        self.pixels = []
        for i in range(self.cols):
            for j in range(self.rows):
                color = self.data[i][j]
                x, y = self.sx + i, self.sy + j
                self.pixels.append([x, y, color])


class TaskManager(object):
    def __init__(self):
        self.tasks = [Task(**kwargs) for kwargs in Const.TASK_tasklist]
        self.pixels = []
        for task in self.tasks:
            self.pixels.extend(task.pixels)
