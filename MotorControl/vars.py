#! /usr/bin/python3
# -*- coding: utf-8 -*-
motorControlInstance = None
qr_directive_executing = False
current_motor_state = [0, 0]
emergency_stop = False
security_motor_override = False

pwm_l = 0
pwm_r = 0