#! /usr/bin/python3
# -*- coding: utf-8 -*-
import system_vars
import Locations.routes as routes
import CamTracking.vars as vars
import CamTracking.util as util
import MotorControl.motor_functions as motor_functions
import settings


def init():
    util.main()


def get_last_barcode():
    return vars.last_barcode


def found_barcode(data):
    import Orders.order_functions as order_functions
    print(system_vars.colorcode['info'] + "INFO: BARCODE DETECTED: " + data + system_vars.colorcode['reset'])
    if data == order_functions.get_current_destination():
        vars.last_barcode = data
        destination_reached()
    else:
        split_data = data.split("-")
        branch_ident = split_data[0]
        branch_direct_ident = split_data[1]
    
        if branch_ident not in vars.last_barcode:
            vars.last_barcode = branch_ident
            print(system_vars.colorcode['info'] + "INFO: NEW LAST BARCODE-BRANCH SET: " + branch_ident + system_vars.colorcode['reset'])
            motor_functions.stop_both()
    
            destination = order_functions.get_current_destination()
            if branch_ident in routes.routes[destination]:
                if branch_direct_ident in routes.routes[destination][branch_ident]:
                    directive = routes.routes[destination][branch_ident][branch_direct_ident]
                    print(system_vars.colorcode['ok'] + "OK: QR-DIRECTIVE: " + directive + system_vars.colorcode['reset'])
                    motor_functions.execute_directive(directive, 'qr')
            else:
                print(system_vars.colorcode['error'] + "ERROR: BRANCH NOT ON ROUTE" + system_vars.colorcode['reset'])
        else:
            print(system_vars.colorcode['info'] + "INFO: BARCODE IGNORED - OF SAME BRANCH AS LAST ONE" + system_vars.colorcode['reset'])
            
            
def destination_reached():
    import Orders.order_functions as order_functions
    order_functions.start_drop_off()
