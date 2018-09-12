from threading import Thread
import RestAPI.main as RestAPI
import SlackBot.main as SlackBot
import MotorControl.util as MotorControl
import glob_vars
import BarCodeRecognition.util as BarCodeRecognition


if __name__ == "__main__":
    glob_vars.motorControlInstance = MotorControl.MotorControl()

    print("INIT")

    SlackBot_thread = Thread(target=SlackBot.main, args=(glob_vars.motorControlInstance,), name="SlackBot", daemon=False)
    SlackBot_thread.start()

    api_thread = Thread(target=RestAPI.start, args=(), name="API", daemon=False)
    api_thread.start()

    BarCode_thread = Thread(target=BarCodeRecognition.main, args=(), name="BarCodeScanner",daemon=False)
    BarCode_thread.start()