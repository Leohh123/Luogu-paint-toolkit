from account import AccountManager
from board import Board
from task import TaskManager
from common import Const, Utils
import threading
import time
import random


class Manager(object):
    def __init__(self):
        self.account_mgr = AccountManager()
        self.board = Board()
        self.task_mgr = TaskManager()
        self.pixels = []

    def add_pixel(self, px):
        if px not in self.pixels:
            self.pixels.append(px)
            Utils.log("[Add]", px)

    def del_pixel(self, px):
        if px in self.pixels:
            self.pixels.remove(px)
            Utils.log("[Del]", px)

    def update_loop(self):
        while True:
            for x, y, color in self.task_mgr.pixels:
                px = [x, y, color]
                if self.board.map[x][y] != color:
                    self.add_pixel(px)
                else:
                    self.del_pixel(px)
            time.sleep(Const.MGR_update_interval)

    def get_pixel(self):
        if len(self.pixels) > 0:
            pos = random.randint(0, len(self.pixels) - 1)
            return self.pixels.pop(pos)
        return None

    def draw_loop(self):
        while True:
            for ac in self.account_mgr.accounts:
                if ac.ready():
                    px = self.get_pixel()
                    if px is not None:
                        ac.draw(*px)
            time.sleep(Const.MGR_draw_interval)

    def count_loop(self):
        while True:
            Utils.log("[Count]", len(self.pixels))
            time.sleep(Const.MGR_count_interval)

    def start(self):
        threading.Thread(target=self.update_loop, daemon=True).start()
        threading.Thread(target=self.draw_loop, daemon=True).start()
        self.count_loop()
