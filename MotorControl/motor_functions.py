from MotorControl import vars
from MotorControl import util
from MotorControl import configuration
import system_vars
import time
from threading import Thread


def init():
    vars.motorControlInstance = util.MotorControl()
    Emergency_Stop_Thread = Thread(target=vars.motorControlInstance.emergency_stop_handler, args=(), name="EmergencyStop", daemon=False)
    Emergency_Stop_Thread.start()


def set_motor(motor, speed):
    vars.motorControlInstance.motor(motor, speed)


def set_motors(speed_l, speed_r):
    vars.motorControlInstance.motor('left', speed_l)
    vars.motorControlInstance.motor('right', speed_r)


def get_motor_state():
    return vars.current_motor_state


def stop_both():
    vars.motorControlInstance.motor('left', 0)
    vars.motorControlInstance.motor('right', 0)


def execute_directive(directive, type):
    if system_vars.remote_control is False:
        if vars.qr_directive_executing is False:
            if type == "qr":
                stop_after_directive = configuration.stop_after_qr_directive
                vars.qr_directive_executing = True
            else:
                stop_after_directive = configuration.stop_after_linetracker_directive

            if directive in configuration.commandIdentifiers:
                curr_l, curr_r = get_motor_state()
                s_l, s_r, duration = configuration.commandIdentifiers[directive]
                set_motors(s_l, s_r)
                if duration is not None:
                    time.sleep(duration)
                    if stop_after_directive:
                        stop_both()
                    else:
                        set_motors(curr_l, curr_r)

            else:
                print(system_vars.colorcode['error'] + "ERROR: MOTOR-CONTROL-FUNCTIONS - UNKNOWN DIRECTIVE-IDENTIFIER" +
                      system_vars.colorcode['reset'])

            vars.qr_directive_executing = False


def set_qr_directive_executing(state):
    vars.qr_directive_executing = state
