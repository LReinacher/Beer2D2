from threading import Thread
from TouchScreen import utils
import time


def init():
    api_thread = Thread(target=utils.start, args=(), name="API", daemon=False)
    api_thread.start()
    time.sleep(1)
    set_order_list([])
    utils.set_info_text('Ready for Order')


def set_ready_order_list(list):
    fill = 7 - len(list)
    fill_list = []

    x = 0
    while x < fill:
        fill_list.append({'name': '----', 'room': '----'})
        x = x + 1

    list.extend(fill_list)

    i = 0
    while i < 6:
        utils.set_item_text('name_' + str(i + 1), list[i]['name'])
        utils.set_item_text('destination_' + str(i + 1), list[i]['room'])
        if list[i]['name'] == "----":
            utils.set_button_enabled('confirm_' + str(i + 1), False)
        else:
            utils.set_button_enabled('confirm_' + str(i + 1), True)
        i = i + 1


def set_order_list(list):
    fill = 7 - len(list)
    fill_list = []

    x = 0
    while x < fill:
        fill_list.append({'name': '----', 'room': '----'})
        x = x + 1

    list.extend(fill_list)

    i = 0
    while i < 6:
        utils.set_item_text('name_' + str(i + 1), list[i]['name'])
        utils.set_item_text('destination_' + str(i + 1), list[i]['room'])
        utils.set_button_enabled('confirm_' + str(i + 1), False)
        i = i + 1


def set_info_text(text):
    utils.set_info_text(text)


def set_button_enabled(item, state):
    utils.set_button_enabled(item, state)


def set_order_confirmed(nr):
    utils.set_button_enabled('confirm_' + str(nr), False)
    utils.set_item_text('confirm_' + str(nr), 'confirmed')


if __name__ == "__main__":
    init()
