from __future__ import division
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
from functools import partial
import UI.vars as vars
import threading, time, sys
import Orders.order_functions as order_functions

qtCreatorFile = "UI/main.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile_DropOff = "UI/drop_off.ui" # Enter file here.
Ui_MainWindow_DropOff, QtBaseClass_DropOff = uic.loadUiType(qtCreatorFile_DropOff)


class workerDropOff(QObject):
    signalDropOff = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def loop(self):
        while True:
            if vars.drop_off_init is True:
                vars.drop_off_init = False
                vars.drop_off = True
                self.signalDropOff.emit()
            time.sleep(.1)


class workerUpdateOrders(QObject):
    signalUpdateOrders = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def loop(self):
        while True:
            if order_functions.get_orders() != vars.old_orders:
                vars.old_orders = order_functions.get_orders()
                self.signalUpdateOrders.emit()
            time.sleep(.1)


class workerUpdateReadyOrderList(QObject):
    signalUpdateReadyOrderList = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def loop(self):
        old_orders = []
        while True:
            if order_functions.get_ready_order_list() != old_orders:
                old_orders = order_functions.get_ready_order_list()
                self.signalUpdateReadyOrderList.emit()
            time.sleep(.1)


class workerUpdateTimer(QObject):
    signalUpdateTimer = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def loop(self):
        old_timer = ""
        while True:
            if order_functions.get_order_countdown() != old_timer:
                old_timer = order_functions.get_order_countdown()
                self.signalUpdateTimer.emit()
            time.sleep(.1)

class MainUI(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        header = self.table.horizontalHeader()
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        header.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        header.setFocusPolicy(QtCore.Qt.NoFocus)

        self.workerDropOff = workerDropOff()
        self.workerDropOffThread = QThread()  # move the Worker object to the Thread object
        self.workerDropOffThread.started.connect(self.workerDropOff.loop)  # init worker loop() at startup
        self.workerDropOff.moveToThread(self.workerDropOffThread)
        self.workerDropOff.signalDropOff.connect(self.signalDropOff)  # Connect your signals/slots
        self.workerDropOffThread.start()

        self.workerUpdateOrders = workerUpdateOrders()
        self.workerUpdateOrdersThread = QThread()  # move the Worker object to the Thread object
        self.workerUpdateOrdersThread.started.connect(self.workerUpdateOrders.loop)  # init worker loop() at startup
        self.workerUpdateOrders.moveToThread(self.workerUpdateOrdersThread)
        self.workerUpdateOrders.signalUpdateOrders.connect(self.signalUpdateOrders)  # Connect your signals/slots
        self.workerUpdateOrdersThread.start()

    def signalDropOff(self):
        show_DropOff_UI()

    def signalUpdateOrders(self):
        self.set_order_list(order_functions.get_orders())

    def set_order_list(self, orders):
        rowPosition = self.table.rowCount()
        if len(orders) == 0:
            i = 0
            while i < rowPosition:
                self.table.removeRow(0)
                i = i + 1
        i = 0
        while i < len(orders):
            if rowPosition <= i:
                self.table.insertRow(rowPosition)
            self.table.setItem(i, 0, QTableWidgetItem(orders[i]["room"]))
            self.table.setItem(i, 1, QTableWidgetItem(orders[i]["real_name"]))
            i = i + 1

    def set_debug_command(self, text):
        self.debug_status.setText(text)


class DropOffUI(QtGui.QMainWindow, Ui_MainWindow_DropOff):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow_DropOff.__init__(self)
        self.setupUi(self)
        header = self.table.horizontalHeader()
        self.table.setColumnWidth(3, 100)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        header.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        header.setFocusPolicy(QtCore.Qt.NoFocus)
        self.confirm_button = {}
        self.set_ready_order_list(order_functions.get_ready_order_list())

        self.workerUpdateReadyOrderList = workerUpdateReadyOrderList()
        self.workerUpdateReadyOrderListThread = QThread()  # move the Worker object to the Thread object
        self.workerUpdateReadyOrderListThread.started.connect(self.workerUpdateReadyOrderList.loop)  # init worker loop() at startup
        self.workerUpdateReadyOrderList.moveToThread(self.workerUpdateReadyOrderListThread)
        self.workerUpdateReadyOrderList.signalUpdateReadyOrderList.connect(self.signalUpdateReadyOrderList)  # Connect your signals/slots
        self.workerUpdateReadyOrderListThread.start()

        self.workerUpdateTimer = workerUpdateTimer()
        self.workerUpdateTimerThread = QThread()  # move the Worker object to the Thread object
        self.workerUpdateTimerThread.started.connect(self.workerUpdateTimer.loop)  # init worker loop() at startup
        self.workerUpdateTimer.moveToThread(self.workerUpdateTimerThread)
        self.workerUpdateTimer.signalUpdateTimer.connect(self.signalUpdateTimer)  # Connect your signals/slots
        self.workerUpdateTimerThread.start()

    def signalUpdateReadyOrderList(self):
        if len(order_functions.get_ready_order_list()) > 0:
            self.set_ready_order_list(order_functions.get_ready_order_list())
        else:
            self.close_window()

    def signalUpdateTimer(self):
        if order_functions.get_order_countdown() == "00:00":
            self.close()
        self.set_counter(order_functions.get_order_countdown())

    def set_ready_order_list(self, orders):
        i = 0
        while i < len(orders):
            rowPosition = self.table.rowCount()
            if rowPosition <= i:
                self.table.insertRow(rowPosition)
            self.table.setItem(i, 0, QTableWidgetItem(orders[i]["real_name"]))
            if orders[i]["open"] is True:
                self.confirm_button[i] = QtGui.QPushButton('Confirm Order')
                self.confirm_button[i].clicked.connect(partial(self.confirm_order,i))
                self.confirm_button[i].setEnabled(True)
            else:
                self.confirm_button[i] = QtGui.QPushButton('confirmed')
                self.confirm_button[i].clicked.connect(partial(self.confirm_order, i))
                self.confirm_button[i].setEnabled(False)
            self.table.setCellWidget(i, 1, self.confirm_button[i])

            i = i + 1

    def confirm_order(self, index):
        self.confirm_button[index].setEnabled(False)
        self.confirm_button[index].setText("confirmed")
        order_functions.confirm_order(index)
        if self.check_all_confirmed():
            self.close_window()

    def check_all_confirmed(self):
        i = 0
        while i < len(order_functions.get_ready_order_list()):
            if order_functions.get_ready_order_list()[i]['open'] is True:
                return False
            i = i + 1
        return True

    def close_window(self):
        vars.dropOff_window_instance = None
        self.close()


    def set_counter(self, time):
        import UI.texts as texts
        self.countdown_label.setText(texts.take_order % time)


def init_UI():
    app = QtGui.QApplication(sys.argv)
    window = MainUI()
    vars.main_window_instance = window
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setFixedSize(800, 480)
    #window.show()
    window.showFullScreen()
    sys.exit(app.exec_())


def show_DropOff_UI():
    window = DropOffUI()
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setFixedSize(800, 480)
    vars.dropOff_window_instance = window
    window.showFullScreen()
