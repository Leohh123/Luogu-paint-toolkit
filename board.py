from common import Const, Utils
from ws import WS
import threading
import time
import requests


class Board(object):
    def __init__(self, callback=None):
        self.callback = callback
        self.size = Const.BOARD_size
        self.width, self.height = self.size
        self.map = []
        self.check()
        self.ws = WS(self.update)
        self.ws.start()
        threading.Thread(target=self.check_loop, daemon=True).start()

    def update(self, x, y, color):
        self.map[x][y] = color
        if self.callback is not None:
            self.callback(x, y, color)

    def check(self):
        r = requests.get(Const.URL_board, headers={
                         "user-agent": Const.NET_user_agent})
        assert r.status_code == 200
        self.map = list(map(lambda t: list(
            map(lambda c: Const.BOARD_chars.find(c), list(t))), r.text.split()))

    def check_loop(self):
        while True:
            try:
                self.check()
                Utils.log("[Board check] ok")
            except:
                Utils.log("[Board check] failed")
            time.sleep(Const.BOARD_check_interval)
