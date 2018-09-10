import SlackBot.util as SlackBot
import MotorControl.util as MotorControl
import time


def main():
    slackCommunication = SlackBot.slackCommunication()
    motor = MotorControl.MotorControl()

    slackCommunication.slackConnect()

    botid = slackCommunication.getBotID("bot")

    slackCommunication.writeToSlack("DCPB13DMX", "Beer2D2 Ready for your order!")["ok"]

    while True:
        communication = slackCommunication.slackReadRTM()
        print(communication)
        if len(communication) > 0:
            try:
                if communication[0]['type'] == 'message' and communication[0]['user'] != botid:
                    message = communication[0]['text']
                    print(message)
                    response = None
                    if message == 'Forwards':
                        motor.forwards()
                        response = 'Going Forwards'
                    elif message == 'Backwards':
                        motor.backwards()
                        response = 'Going Backwards'
                    elif message == 'Left':
                        motor.left()
                        response = 'Turning Left'
                    elif message == 'Right':
                        motor.right()
                        response = 'Turning Right'
                    elif message == 'Stop':
                        motor.stop()
                        response = 'Standing Still'
                    elif message == 'Shut Down':
                        response = 'Shutting Down'
                    elif message == 'Command not found! Available Commands: Forwards, Backwards, Left, Right, Stop':
                        pass
                    elif message == 'Beer2D2 Ready for your order!':
                        pass
                    else:
                        response = 'Command not found! Available Commands: Forwards, Backwards, Left, Right, Stop'
                    if response is not None:
                        slackCommunication.writeToSlack(communication[0]['user'], response)["ok"]

            except Exception as e:
                print('ERROR')
        time.sleep(0.5)



if __name__ == "__main__":
    main()