#! /usr/bin/python3
# -*- coding: utf-8 -*-
touchscreenInstance = None
BuildInstance = None

builder = None

screen_data = {
    'info_label': {'text': 'Ready for your order'},
    'destination_1': {'text': '----'},
    'destination_2': {'text': '----'},
    'destination_3': {'text': '----'},
    'destination_4': {'text': '----'},
    'destination_5': {'text': '----'},
    'destination_6': {'text': '----'},
    'name_1': {'text': '----'},
    'name_2': {'text': '----'},
    'name_3': {'text': '----'},
    'name_4': {'text': '----'},
    'name_5': {'text': '----'},
    'name_6': {'text': '----'},
    'confirm_1': {'enabled': False, 'label': '----'},
    'confirm_2': {'enabled': False, 'label': '----'},
    'confirm_3': {'enabled': False, 'label': '----'},
    'confirm_4': {'enabled': False, 'label': '----'},
    'confirm_5': {'enabled': False, 'label': '----'},
    'confirm_6': {'enabled': False, 'label': '----'}

    }

screen_data_old = {
    'info_label': {'text': None},
    'destination_1': {'text': None},
    'destination_2': {'text': None},
    'destination_3': {'text': None},
    'destination_4': {'text': None},
    'destination_5': {'text': None},
    'destination_6': {'text': None},
    'name_1': {'text': None},
    'name_2': {'text': None},
    'name_3': {'text': None},
    'name_4': {'text': None},
    'name_5': {'text': None},
    'name_6': {'text': None},
    'confirm_1': {'enabled': None, 'label': None},
    'confirm_2': {'enabled': None, 'label': None},
    'confirm_3': {'enabled': None, 'label': None},
    'confirm_4': {'enabled': None, 'label': None},
    'confirm_5': {'enabled': None, 'label': None},
    'confirm_6': {'enabled': None, 'label': None}
    }

objects = {
    'info_label': None,
    'destination_1': None,
    'destination_2': None,
    'destination_3': None,
    'destination_4': None,
    'destination_5': None,
    'destination_6': None,
    'name_1': None,
    'name_2': None,
    'name_3': None,
    'name_4': None,
    'name_5': None,
    'name_6': None,
    'confirm_1': None,
    'confirm_2': None,
    'confirm_3': None,
    'confirm_4': None,
    'confirm_5': None,
    'confirm_6': None
}
