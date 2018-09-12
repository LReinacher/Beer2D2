#settings
stop_after_qr_directive = True
stop_after_linetracker_directive = False

#Motortimes in Seconds
light_turn_time = 0.2
half_turn_time = 0.5
full_turn_time = 1
full_spin_time = 0.5
straight_time = 1

#CommandIdentifiers
commandIdentifiers = { #[left_motor_command, right_motor_command, duration]]
    'light_left_turn': ['stop', 'forwards', light_turn_time],
    'light_right_turn': ['forwards', 'stop', light_turn_time],
    'half_left_turn': ['stop', 'forwards', half_turn_time],
    'half_right_turn': ['forwards', 'stop', half_turn_time],
    'full_left_turn': ['stop', 'forwards', full_turn_time],
    'full_right_turn': ['forwards', 'stop', full_turn_time],
    'full_left_spin': ['backwards', 'forwards', full_spin_time],
    'full_right_spin': ['forwards', 'backwards', full_spin_time],
    'straight': ['forwards', 'forwards', straight_time],
    'forwards': ['forwards', 'forwards', None],
    'backwards': ['backwards', 'backwards', None],
    'stop': ['stop', 'stop', None],
}
