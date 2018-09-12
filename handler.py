import glob_vars
import routes

def found_barcode(data):
    if data not in glob_vars.last_barcode:
        glob_vars.last_barcode = data

        motorControl = glob_vars.motorControlInstance
        print("BAR-CODE FOUND: " + data)
        motorControl.stop()

        split_data = data.split("-")
        branch_ident = split_data[0]
        branch_direct_ident = split_data[1]
        if branch_ident in routes.routes[glob_vars.current_destination]:
            if branch_ident in routes.routes[glob_vars.current_destination][branch_ident]:
                directive = routes.routes[glob_vars.current_destination][branch_ident][branch_direct_ident]
                print(directive)
    else:
        #print("Barcode of this Branch already Scanned")
        pass



