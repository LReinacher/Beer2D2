import SlackBot.util as SlackBot
import time
from SlackBot import vars
from Orders import order_functions
from Locations import location_functions
from SlackBot import responses
import system_vars

def init():
    vars.SlackBotInstance = SlackBot.slackCommunication()
    vars.members_email, vars.members_id = load_member_emails()
    print(system_vars.colorcode['ok'] + "OK: SLACK-BOT INITIALIZED" + system_vars.colorcode['reset'])
    message_handling()


def load_member_emails():
    members_email = {}
    members_id = {}
    slackCommunication = vars.SlackBotInstance
    slackCommunication.slackConnect()
    result = slackCommunication.getTeamList()
    memberNr = 0
    while memberNr < len(result['members']):
        if 'email' in result['members'][memberNr]['profile']:
            email = result['members'][memberNr]['profile']['email']
            id = result['members'][memberNr]['id']
            if 'real_name' in result['members'][memberNr]['profile']:
                real_name = result['members'][memberNr]['profile']['real_name']
            else:
                real_name = "Unnamed User"
            members_email[email] = {'id': id, 'real_name': real_name}
            members_id[id] = {'email': email, 'real_name': real_name}
        memberNr = memberNr + 1
    return members_email, members_id


def get_real_name(user, type):
    if type == "slack":
        return vars.members_id[user]['real_name']
    else:
        return vars.members_email[user]['real_name']


def get_id_by_email(email):
    if email in vars.members_email:
        return vars.members_email[email]['id']
    else:
        return None


def get_email_by_id(id):
    if id in vars.members_id:
        return vars.members_id[id]['email']
    else:
        return None


def send_dm(user, message):
    return vars.SlackBotInstance.create_send_dm(user, message)



def message_handling():
    print(system_vars.colorcode['ok'] + "OK: SLACK-BOT STARTED" + system_vars.colorcode['reset'])
    slackCommunication = vars.SlackBotInstance

    slackCommunication.slackConnect()

    bot_user_id = "UCQ3C8M5K"

    while True:
        communication = slackCommunication.slackReadRTM()
        if len(communication) > 0:
            try:
                if communication[0]['type'] == 'message' and communication[0]['user'] != bot_user_id:
                    message = communication[0]['text']
                    print(system_vars.colorcode['info'] + "INFO: SLACK MESSAGE: " + message + system_vars.colorcode['reset'])
                    if 'come to' in message:
                        split = message.split(' ')
                        try:
                            location = split[2]
                            if location_functions.check_for_location(location):
                                status, order = order_functions.add_order(communication[0]['user'], location, 'slack')
                                if status:
                                    response = (responses.order_placed_success % str(order + 1))
                                else:
                                    if order['type'] == "slack":
                                        order_type = responses.slack_interface_name
                                    else:
                                        order_type = responses.web_interface_name
                                    order_location = order['room']
                                    response = (responses.order_placed_error_already_placed % (order_type, order_location))
                            else:
                                response = responses.order_placed_error_location_not_available
                        except:
                            response = responses.order_placed_error_location_invalid

                    elif 'cancel order' in message:
                        if order_functions.delete_oder(communication[0]['user'], 'slack'):
                            response = responses.order_cancel_success
                        else:
                            response = responses.error_no_open_order
                    elif 'confirm delivery' in message:
                        email = get_email_by_id(communication[0]['user'])
                        index = order_functions.check_user_order(communication[0]['user'], email)
                        if index >= 0:
                            order_functions.delete_oder(communication[0]['user'], 'slack')
                            response = responses.order_marked_delivered_success
                        else:
                            response = responses.error_no_open_order
                    elif 'list orders' in message:
                        orders = order_functions.get_orders()
                        if len(orders) > 0:
                            orders_string = ""
                            i = 0
                            while i < len(orders):
                                orders_string = orders_string + "\n `" + str(i + 1) + ". " + orders[i]['room'] + " - " + orders[i]['real_name'] + "`"
                                i = i + 1
                            response = (responses.current_orders % orders_string)
                        else:
                            response = responses.no_current_orders
                    elif 'list locations' in message:
                        locations = location_functions.get_locations()
                        location_string = ""
                        for location in locations:
                            location_string = location_string + "\n • `" + location + "`"
                        response = (responses.list_locations % location_string)
                    elif 'hello' in message:
                        response = (responses.hello_message % responses.available_commands)
                    else:
                        response = (responses.command_not_found % responses.available_commands)
                    if response is not None:
                        result = slackCommunication.writeToSlack(communication[0]['user'], response)["ok"]

            except Exception as e:
                print(system_vars.colorcode['error'] + "ERROR: SLACK-BOT-FUNCTIONS " + str(e).upper() + system_vars.colorcode['reset'])
        time.sleep(0.5)
