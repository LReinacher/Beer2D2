#! /usr/bin/python3
# -*- coding: utf-8 -*-

last_command_time = None
security_stopped = False
security_stop_timer = 2 #sec

last_active_command_time = None
inactivity_timer = 30 #sec

api_public = ""
api_private = ""

remote_control = False
remote_control_user = None

order_que = []