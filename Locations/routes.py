#! /usr/bin/python3
# -*- coding: utf-8 -*-
routes = {
    "Morty": {
        "001": {"A": "half_left_turn", "B": "straight", "C": "full_left_spin"},
        "002": {"A": "half_left_turn", "B": "straight", "C": "full_left_spin"},
    },
    "No Destination": {
        "001": {"A": "half_left_turn", "B": "straight", "C": "full_left_spin"},
        "002": {"A": "half_left_turn", "B": "straight", "C": "full_left_spin"},
    }

}

leave_procedure = { #destination_identifer: [{command: duration}]
    'Morty': [{'backwards': 2, 'full_turn': None}],
    'No Destination': [{'backwards': 2, 'full_turn': None}],
}
