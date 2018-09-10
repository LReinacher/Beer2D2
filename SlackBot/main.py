import SlackBot.util as SlackBot
import time


def main(motor):
    slack_duration_identifier = ":"
    bot_user_id = "UCQ3C8M5K"

    slackCommunication = SlackBot.slackCommunication()

    slackCommunication.slackConnect()

    slackCommunication.writeToSlack("DCPB13DMX", "Beer2D2 Ready for your order!")["ok"]

    while True:
        communication = slackCommunication.slackReadRTM()
        print(communication)
        if len(communication) > 0:
            try:
                if communication[0]['type'] == 'message' and communication[0]['user'] != bot_user_id:
                    message = communication[0]['text']
                    print(message)
                    response = None
                    if 'Forwards' in message:
                        if slack_duration_identifier in message:
                            split = message.split(slack_duration_identifier)
                            try:
                                duration = float(split[1])
                                slackCommunication.writeToSlack(communication[0]['user'], 'Going Forwards for ' + str(duration) + ' Seconds')["ok"]
                                motor.forwards(duration)
                                response = None
                            except:
                                response = 'Invalid Duration'
                        else:
                            motor.forwards()
                            response = 'Going Forwards'
                    elif 'Backwards' in message:
                        if slack_duration_identifier in message:
                            split = message.split(slack_duration_identifier)
                            try:
                                duration = float(split[1])
                                slackCommunication.writeToSlack(communication[0]['user'], 'Going Backwards for ' + str(duration) + ' Seconds')["ok"]
                                motor.forwards(duration)
                                response = None
                            except:
                                response = 'Invalid Duration'
                        else:
                            motor.backwards()
                            response = 'Going Backwards'
                    elif 'Spin Left' in message:
                        if slack_duration_identifier in message:
                            split = message.split(slack_duration_identifier)
                            try:
                                duration = float(split[1])
                                slackCommunication.writeToSlack(communication[0]['user'], 'Spinning Left for ' + str(duration) + ' Seconds')["ok"]
                                motor.forwards(duration)
                                response = None
                            except:
                                response = 'Invalid Duration'
                        else:
                            motor.spin_left()
                            response = 'Spinning Left'
                    elif 'Spin Right' in message:
                        if slack_duration_identifier in message:
                            split = message.split(slack_duration_identifier)
                            try:
                                duration = float(split[1])
                                slackCommunication.writeToSlack(communication[0]['user'], 'Spinning Right for ' + str(duration) + ' Seconds')["ok"]
                                motor.forwards(duration)
                                response = None
                            except:
                                response = 'Invalid Duration'
                        else:
                            motor.spin_right()
                            response = 'Spinning Right'
                    elif 'Turn Left' in message:
                        if slack_duration_identifier in message:
                            split = message.split(slack_duration_identifier)
                            try:
                                duration = float(split[1])
                                slackCommunication.writeToSlack(communication[0]['user'], 'Turning Left for ' + str(duration) + ' Seconds')["ok"]
                                motor.forwards(duration)
                                response = None
                            except:
                                response = 'Invalid Duration'
                        else:
                            motor.turn_left()
                            response = 'Turning Left'
                    elif 'Turn Right' in message:
                        if slack_duration_identifier in message:
                            split = message.split(slack_duration_identifier)
                            try:
                                duration = float(split[1])
                                slackCommunication.writeToSlack(communication[0]['user'], 'Turning Right for ' + str(duration) + ' Seconds')["ok"]
                                motor.forwards(duration)
                                response = None
                            except:
                                response = 'Invalid Duration'
                        else:
                            motor.turn_right()
                            response = 'Turning Right'
                    elif 'Stop' in message:
                        motor.stop()
                        response = 'Standing Still'
                    elif message == 'Shut Down':
                        response = 'Shutting Down'
                    else:
                        response = 'Command not found! Available Commands: Forwards, Backwards, Turn Left, Turn Right, Spin Left, Spin Right, Stop + (:TimeInSecounds)'
                    if response is not None:
                        slackCommunication.writeToSlack(communication[0]['user'], response)["ok"]

            except Exception as e:
                print('ERROR')
        time.sleep(0.5)
