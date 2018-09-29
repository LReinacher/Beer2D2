#! /usr/bin/python3
# -*- coding: utf-8 -*-
import settings

web_interface_name = " the web-interface"
slack_interface_name = "Slack"

order_placed_success = "Your order has been placed. It is at position %s"
order_placed_error_already_placed = "You already placed an order via %s to %s"
order_placed_error_location_not_available = "Sorry, but that location is not available"
order_placed_error_location_invalid = "Error: location invalid"

error_no_open_order = "You do not have an open order at the moment"

order_cancel_success = "Your order was canceled successfully"

order_marked_delivered_success = "Your order was marked as delivered. I hope you are satisfied with my service."

current_orders = "Current orders: %s "
no_current_orders = "There are no orders at the moment."

list_locations = "Available locations: %s \n Use `come to <location>` to call " + settings.name + " to that location (e.g. `come to Morty`)"

hello_message = "Hi there CODEianer!\n I am " + settings.name + " - the campus-fridge that comes to you!\n You can interact with me by using the following commands: %s \n So, how can I be of service?"

available_commands = "\n • `come to <location>` - call " + settings.name + " to your desired location (e.g. `come to Morty`)\n • `list locations` - get a list of all available locations\n • `cancel order` - cancel your current order\n • `confirm delivery` - confirm the delivery of your order\n • `list orders` - get a list of all current orders"

command_not_found = "Command not found! Available commands: %s"

order_ready = "Your order is ready to be picked up! \nYou have %s left to do so!"