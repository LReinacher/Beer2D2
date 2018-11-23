#! /usr/bin/python3
# -*- coding: utf-8 -*-
remote_control_key = None

last_command_time = None
security_stopped = False
security_stop_timer = 2 #sec

last_active_command_time = None
inactivity_timer = 30 #sec

#SECRET KEYS
secret_keys = {'add_order': '45Aa*+=H5Nc_NdLm',
               'cancel_order': '^SF%NqDZB8av_KbB',
               'confirm_order': 'EdHD&k5X$y4UTv%z',
               'enable_remote': '@Qzc?UwqkVbh5z@W',
               'update_remote_control_status': 'A5_8umdWZd84RLar',
               'update_order_list': 'yYRJ6=P*H9e7x^nA',
               'update_last_barcode': '9qm*YAG#rQJK+fY^'}

interface_api_url = "http://192.168.2.143:8000/api"
