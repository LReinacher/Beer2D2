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
    'light_left_turn': [0, 15, light_turn_time],
    'light_right_turn': [15, 0, light_turn_time],
    'half_left_turn': [0, 15, half_turn_time],
    'half_right_turn': [15, 0, half_turn_time],
    'full_left_turn': [0, 15, full_turn_time],
    'full_right_turn': [15, 0, full_turn_time],
    'full_left_spin': [-15, 15, full_spin_time],
    'full_right_spin': [15, -15, full_spin_time],
    'straight': [15, 15, straight_time],

    'stop': [0, 0, None],
    'forwards': [15, 15, None],
    'backwards': [-15, -15, None],

    'left_1': [14, 15, None],
    'left_2': [13, 15, None],
    'left_3': [12, 15, None],
    'left_4': [10, 15, None],
    'left_5': [8, 15, None],
    'left_6': [5, 15, None],
    'left_7': [3, 15, None],
    'left_8': [0, 15, None],
    'right_1': [15, 14, None],
    'right_2': [15, 13, None],
    'right_3': [15, 12, None],
    'right_4': [15, 10, None],
    'right_5': [15, 8, None],
    'right_6': [15, 5, None],
    'right_7': [15, 3, None],
    'right_8': [15, 0, None],

    'spin': [5, -5, None]
}

tracking_min_speed = 4
tracking_mid_speed = 7
tracking_max_speed = 10

speedIdentifiers = { #[PWM-frequency in Hz, gear_relai_mode (fwd / bwd)]
    0: [0, 'fwd'],
    1: [100, 'fwd'],
    2: [110, 'fwd'],
    3: [120, 'fwd'],
    4: [130, 'fwd'],
    5: [140, 'fwd'],
    6: [150, 'fwd'],
    7: [160, 'fwd'],
    8: [170, 'fwd'],
    9: [180, 'fwd'],
    10: [190, 'fwd'],
    11: [200, 'fwd'],
    12: [210, 'fwd'],
    13: [220, 'fwd'],
    14: [230, 'fwd'],
    15: [240, 'fwd'],
    16: [255, 'fwd'],
    -1: [100, 'bwd'],
    -2: [110, 'bwd'],
    -3: [120, 'bwd'],
    -4: [130, 'bwd'],
    -5: [140, 'bwd'],
    -6: [150, 'bwd'],
    -7: [160, 'bwd'],
    -8: [170, 'bwd'],
    -9: [180, 'bwd'],
    -10: [190, 'bwd'],
    -11: [200, 'bwd'],
    -12: [210, 'bwd'],
    -13: [220, 'bwd'],
    -14: [230, 'bwd'],
    -15: [240, 'bwd'],
    -16: [255, 'bwd'],
}
