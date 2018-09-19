from Locations import vars


def get_locations():
    return vars.locations


def check_for_location(location):
    if location in vars.locations:
        return True
    return False

