from common import Const, Utils
import websocket
import threading
import json
import time


class WS(object):
    def __init__(self, update_func):
        self.update_func = update_func
        self.msg_flag = True

    def start(self):
        def on_open(ws):
            Utils.log("### open ###")
            message = {
                "type": "join_channel",
                "channel": "paintboard",
                "channel_param": ""
            }
            ws.send(json.dumps(message))

        def on_message(ws, message):
            data = json.loads(message)
            if data["type"] == "paintboard_update":
                self.msg_flag = True
                self.update_func(data["x"], data["y"], data["color"])

        def on_error(ws, error):
            Utils.log("### error ###")
            Utils.log(error)
            connect()

        def on_close(ws):
            Utils.log("### closed ###")

        def _connect():
            websocket.enableTrace(True)
            self.ws = websocket.WebSocketApp(
                Const.URL_wss,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            self.ws.run_forever(
                ping_interval=Const.WS_ping_interval,
                ping_timeout=Const.WS_ping_timeout
            )

        def connect():
            threading.Thread(target=_connect, daemon=True).start()

        def check_loop():
            while True:
                print("### WS check ###")
                if self.msg_flag:
                    self.msg_flag = False
                else:
                    self.ws.close()
                    self.msg_flag = True
                    connect()
                time.sleep(Const.WS_check_interval)

        connect()
        threading.Thread(target=check_loop, daemon=True).start()


if __name__ == "__main__":
    ws = WS(print)
    ws.start()
    time.sleep(1 << 16)
