#! /usr/bin/python3
# -*- coding: utf-8 -*-
from Locations import vars
import system_vars
from Locations import routes
from MotorControl import motor_functions


def get_locations():
    return vars.locations


def check_for_location(location):
    if location in vars.locations:
        return True
    return False


def leave_location(location):
    if location in routes.leave_procedure:
        i = 0
        while i < routes.leave_procedure[location]:
            for key in routes.leave_procedure[location][i]:
                motor_functions.execute_directive(key, 'leave', routes.leave_procedure[location][i][key])

    system_vars.destination_reached = False

