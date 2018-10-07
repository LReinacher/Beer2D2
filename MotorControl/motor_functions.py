#! /usr/bin/python3
# -*- coding: utf-8 -*-
import MotorControl.vars as vars
import MotorControl.util as util
import MotorControl.configuration as configuration
import system_vars
import time
from threading import Thread


def init():
    vars.motorControlInstance = util.MotorControl()
    Emergency_Stop_Thread = Thread(target=vars.motorControlInstance.emergency_stop_and_door_status_handler, args=(), name="EmergencyStop_DoorOpen_Handler", daemon=False)
    Emergency_Stop_Thread.start()


def set_motor(motor, speed, security_override=False):
    if vars.security_motor_override is False or security_override is True:
        vars.motorControlInstance.motor(motor, speed)
    else:
        print(system_vars.colorcode['warning'] + "WARNING: SECURITY MOTOR OVERRIDE" +
              system_vars.colorcode['reset'])


def set_motors_api(speed_l, speed_r):
    try:
        speed_l = float(speed_l)
    except:
        return 3

    try:
        speed_r = float(speed_r)
    except:
        return 4

    if speed_l in configuration.speedIdentifiers:
        if speed_r in configuration.speedIdentifiers:
            set_motors(speed_l, speed_r)
            return 0
        else:
            return 2
    else:
        return 1


def set_motors(speed_l, speed_r, security_override=False):
    set_motor('left', speed_l, security_override)
    set_motor('right', speed_r, security_override)


def get_motor_state():
    return vars.current_motor_state


def stop_both(security_override=False):
    set_motor('left', 0, security_override)
    set_motor('right', 0, security_override)


def execute_directive(directive, type, custom_duration=None, speed=None):
    #print(directive)
    speed_multiplier = 1
    if system_vars.remote_control is False:
        if type == "leave":
            stop_after_directive = True
        elif vars.qr_directive_executing is False and system_vars.destination_reached is False and system_vars.door_is_open is False:
            if type == "qr":
                stop_after_directive = configuration.stop_after_qr_directive
                vars.qr_directive_executing = True
            else:
                stop_after_directive = configuration.stop_after_linetracker_directive
                #print('Speed:' + str(speed))
                if speed == 1:
                    speed_multiplier = configuration.tracking_min_speed / 15
                elif speed == 2:
                    speed_multiplier = configuration.tracking_mid_speed / 15
                else:
                    speed_multiplier = configuration.tracking_max_speed / 15
        elif system_vars.door_is_open:
            stop_both()
            print(system_vars.colorcode['warning'] + "WARNING: MOTOR STOPPED - DOOR IS OPEN" +
                  system_vars.colorcode['reset'])
            return False
        else:
            return False

        if directive in configuration.commandIdentifiers:
            curr_l, curr_r = get_motor_state()
            s_l, s_r, duration = configuration.commandIdentifiers[directive]
            s_l = int(s_l * speed_multiplier)
            s_r = int(s_r * speed_multiplier)
            print(speed_multiplier)
            if custom_duration is not None:
                duration = custom_duration
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

