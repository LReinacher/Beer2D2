import glob_vars
import routes


def found_barcode(data):
    print("last:" + glob_vars.last_barcode)

    split_data = data.split("-")
    branch_ident = split_data[0]
    branch_direct_ident = split_data[1]

    if branch_ident not in glob_vars.last_barcode:
        glob_vars.last_barcode = branch_ident
        print("new last:" + glob_vars.last_barcode)

        motorControl = glob_vars.motorControlInstance
        print("BAR-CODE FOUND: " + data)
        motorControl.stop()

        if branch_ident in routes.routes[glob_vars.current_destination]:
            if branch_direct_ident in routes.routes[glob_vars.current_destination][branch_ident]:
                directive = routes.routes[glob_vars.current_destination][branch_ident][branch_direct_ident]
                if glob_vars.remote_system_motor_override is False:
                    motorControl.execute_qr_directive(directive)
                    print('QR-Directive: ' + directive)
    else:
        pass





