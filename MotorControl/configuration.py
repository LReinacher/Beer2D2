#! /usr/bin/python3
# -*- coding: utf-8 -*-

#settings
stop_after_qr_directive = True
stop_after_linetracker_directive = False
pwm_mode = True

#Motortimes in Seconds
light_turn_time = 0.2
half_turn_time = 0.5
full_turn_time = 1
full_spin_time = 0.5
straight_time = 1

#CommandIdentifiers
commandIdentifiers = { #[left_motor_command, right_motor_command, duration]]
    'light_left_turn': [0, 1, light_turn_time],
    'light_right_turn': [1, 0, light_turn_time],
    'half_left_turn': [0, 1, half_turn_time],
    'half_right_turn': [1, 0, half_turn_time],
    'full_left_turn': [0, 1, full_turn_time],
    'full_right_turn': [1, 0, full_turn_time],
    'full_left_spin': [-1, 1, full_spin_time],
    'full_right_spin': [1, -1, full_spin_time],
    'straight': [1, 1, straight_time],
    'forwards': [1, 1, None],
    'backwards': [-1, -1, None],
    'stop': [0, 0, None],
}

speedIdentifiers = { #[PWM-frequency in Hz, gear_relai_mode (fwd / bwd)]
    0: [0, 'fwd'],
    1: [10, 'fwd'],
    2: [20, 'fwd'],
    3: [30, 'fwd'],
    4: [40, 'fwd'],
    5: [50, 'fwd'],
    6: [60, 'fwd'],
    7: [70, 'fwd'],
    8: [80, 'fwd'],
    9: [90, 'fwd'],
    10: [100, 'fwd'],
    11: [110, 'fwd'],
    12: [120, 'fwd'],
    13: [130, 'fwd'],
    14: [140, 'fwd'],
    15: [150, 'fwd'],
    16: [160, 'fwd'],
    17: [170, 'fwd'],
    18: [180, 'fwd'],
    19: [190, 'fwd'],
    20: [200, 'fwd'],
    21: [210, 'fwd'],
    22: [220, 'fwd'],
    23: [230, 'fwd'],
    24: [240, 'fwd'],
    25: [250, 'fwd'],
    -1: [10, 'bwd'],
    -2: [20, 'bwd'],
    -3: [30, 'bwd'],
    -4: [40, 'bwd'],
    -5: [50, 'bwd'],
    -6: [60, 'bwd'],
    -7: [70, 'bwd'],
    -8: [80, 'bwd'],
    -9: [90, 'bwd'],
    -10: [100, 'bwd'],
    -11: [110, 'bwd'],
    -12: [120, 'bwd'],
    -13: [130, 'bwd'],
    -14: [140, 'bwd'],
    -15: [150, 'bwd'],
    -16: [160, 'bwd'],
    -17: [170, 'bwd'],
    -18: [180, 'bwd'],
    -19: [190, 'bwd'],
    -20: [200, 'bwd'],
    -21: [210, 'bwd'],
    -22: [220, 'bwd'],
    -23: [230, 'bwd'],
    -24: [240, 'bwd'],
    -25: [250, 'bwd'],
}
