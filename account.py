from common import Const, Utils
from datetime import datetime
import requests
import threading
import time


class Account(object):
    def __init__(self, uid, cookie_str):
        self.uid = uid
        cookie = dict(map(lambda t: t.split("="), cookie_str.split("; ")))
        self.ss = requests.Session()
        self.ss.cookies = requests.utils.cookiejar_from_dict(cookie)
        self.ss.headers.update({"user-agent": Const.NET_user_agent})
        self.last_upd_time = 0.0

    def ready(self):
        cur_time = datetime.now().timestamp()
        return (cur_time - self.last_upd_time) > Const.ACT_cooldown

    def draw(self, x, y, color):
        data = {"x": x, "y": y, "color": color}
        r = self.ss.post(Const.URL_paint, data)
        if r.status_code == 200:
            self.last_upd_time = datetime.now().timestamp()
            Utils.log("[OK]", self.uid, data, r.text, self.last_upd_time)
            return True
        Utils.log("[Fail]", self.uid, data, r.status_code, r.text)
        return False


class AccountManager(object):
    def __init__(self):
        self.accounts = [Account(u, c) for u, c in Const.ACT_cookies]
