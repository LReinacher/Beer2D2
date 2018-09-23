#settings
stop_after_qr_directive = True
stop_after_linetracker_directive = False
pwm_mode = False

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
    2: [200, 'fwd'],
    3: [300, 'fwd'],
    4: [400, 'fwd'],
    5: [500, 'fwd'],
    6: [600, 'fwd'],
    7: [700, 'fwd'],
    8: [800, 'fwd'],
    9: [900, 'fwd'],
    10: [1000, 'fwd'],
    -1: [100, 'bwd'],
    -2: [200, 'bwd'],
    -3: [300, 'bwd'],
    -4: [400, 'bwd'],
    -5: [500, 'bwd'],
    -6: [600, 'bwd'],
    -7: [700, 'bwd'],
    -8: [800, 'bwd'],
    -9: [900, 'bwd'],
    -10: [1000, 'bwd'],
}