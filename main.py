import SlackBot.util as SlackBot
import MotorControl.util as MotorControl
import time


def main():
    slackCommunication = SlackBot.slackCommunication()
    motor = MotorControl.MotorControl()

    botid = slackCommunication.getBotID("bot")

    slackCommunication.slackConnect()

    slackCommunication.writeToSlack("DCPB13DMX", "Beer2D2 Ready for your order!")["ok"]

    while True:
        communication = slackCommunication.slackReadRTM()
        print(communication)
        if len(communication) > 0:
            try:
                if communication[0]['type'] == 'message' and communication[0]['user'] != botid:
                    message = communication[0]['text']
                    print(message)
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
                    else:
                        response = 'Command not found! Available Commands: Forwards, Backwards, Left, Right, Stop'
                    slackCommunication.writeToSlack(communication[0]['user'], response)["ok"]

            except:
                print('ERROR')
        time.sleep(1)



if __name__ == "__main__":
    main()