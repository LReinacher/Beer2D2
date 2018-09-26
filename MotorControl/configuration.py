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
