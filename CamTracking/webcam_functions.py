import system_vars
from Locations import routes
from CamTracking import vars
from CamTracking import util
from MotorControl import motor_functions
from Orders import order_functions


def init():
    util.main()


def found_barcode(data):
    print(system_vars.colorcode['info'] + "INFO: BARCODE DETECTED: " + data + system_vars.colorcode['reset'])
    split_data = data.split("-")
    branch_ident = split_data[0]
    branch_direct_ident = split_data[1]

    if branch_ident not in vars.last_barcode:
        system_vars.last_barcode = branch_ident
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