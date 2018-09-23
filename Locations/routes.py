#! /usr/bin/python3
# -*- coding: utf-8 -*-
routes = {
    "Morty": {
        "001": {"A": "half_right_turn", "B": "full_right_spin", "C": "straight"},
        "002": {"A": "half_left_turn", "B": "straight", "C": "full_right_spin"},
    }

}

leave_procedure = { #destination_identifer: [{command: duration}]
    'Morty': [{'backwards': 2, 'full_turn': None}],
}
