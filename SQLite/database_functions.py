import sqlite3
from datetime import datetime


def upload_order(location, user):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()

    c.execute("INSERT INTO orders VALUES (%s, %s, %s ,False, False, False)" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user, location))
    conn.commit()

    conn.close()


def set_delivered(user):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()

    c.execute("UPDATE orders SET delivered = True WHERE user = '%s' AND date = (SELECT MAX(date) FROM orders WHERE user = %s)" % (user, user))
    conn.commit()

    conn.close()


def set_confirmed(user):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()

    c.execute(
        "UPDATE orders SET confirmed = True WHERE user = '%s' AND date = (SELECT MAX(date) FROM orders WHERE user = %s)" % (user, user))
    conn.commit()

    conn.close()


def set_canceled(user):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()

    c.execute(
        "UPDATE orders SET canceled = True WHERE user = '%s' AND date = (SELECT MAX(date) FROM orders WHERE user = %s)" % (user, user))
    conn.commit()

    conn.close()
