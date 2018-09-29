import UI.util as util
from threading import Thread
import time
import UI.vars as vars


def init():
    util.init_UI()


def start_drop_off():
    vars.drop_off_init = True


def force_order_update():
    vars.old_orders = ["1", "2"]


if __name__ == "__main__":
    SlackBot_thread = Thread(target=init, args=(), name="SlackBot", daemon=False)
    SlackBot_thread.start()
    time.sleep(3)
    vars.drop_off_init = True
    time.sleep(1)
    vars.pickup_timer = "00:03"
    time.sleep(1)
    vars.pickup_timer = "00:02"
    time.sleep(1)
    vars.pickup_timer = "00:01"
    time.sleep(1)
    vars.pickup_timer = "00:00"
    time.sleep(1)
    vars.ready_orders = [{'real_name': 'Lion Reinacher', 'open': False, 'room': "Morty"}, {'real_name': 'Lion LLOL', 'open': True, 'room': "Rick"}]