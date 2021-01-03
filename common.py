import json


class Const(object):
    URL_board = "https://www.luogu.com.cn/paintBoard/board"
    URL_paint = "https://www.luogu.com.cn/paintBoard/paint"
    URL_wss = "wss://ws.luogu.com.cn/ws"
    NET_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    WS_ping_interval = 60
    WS_ping_timeout = 5
    WS_check_interval = 60
    ACT_cooldown = 31.0
    ACT_cookies = []
    PA_method = "average"
    PA_colors = [
        (0, 0, 0), (255, 255, 255), (170, 170, 170), (85, 85, 85),
        (254, 211, 199), (255, 196, 206), (250, 172, 142), (255, 139, 131),
        (244, 67, 54), (233, 30, 99), (226, 102, 158), (156, 39, 176),
        (103, 58, 183), (63, 81, 181), (0, 70, 112), (5, 113, 151),
        (33, 150, 243), (0, 188, 212), (59, 229, 219), (151, 253, 220),
        (22, 115, 0), (55, 169, 60), (137, 230, 66), (215, 255, 7),
        (255, 246, 209), (248, 203, 140), (255, 235, 59), (255, 193, 7),
        (255, 152, 0), (255, 87, 34), (184, 63, 39), (121, 85, 72)
    ]
    BOARD_size = [1000, 600]
    BOARD_check_interval = 60
    BOARD_chars = "0123456789abcdefghijklmnopqrstuv"
    TASK_tasklist = []
    MGR_update_interval = 0.2
    MGR_draw_interval = 0.1
    MGR_count_interval = 40
    UI_scale = 1
    UI_check_interval = 10
    UI_flush_interval = 0.1
    UI_max_magnification = 5

    @classmethod
    def __init__(cls):
        with open("./config.json") as f:
            cfg = json.loads(f.read())
            cls.ACT_cookies = cfg["cookies"]
            cls.TASK_tasklist = cfg["tasklist"]


Const.__init__()


class Utils(object):
    @staticmethod
    def array2d(x, y, default=None):
        if callable(default):
            return [[default() for j in range(y)] for i in range(x)]
        return [[default for j in range(y)] for i in range(x)]

    @staticmethod
    def log(*args):
        print(*args)

    @staticmethod
    def interval(l, r, x):
        return min(r, (max(l, x)))

    @staticmethod
    def in_interval(l, r, x):
        return l <= x and x <= r
