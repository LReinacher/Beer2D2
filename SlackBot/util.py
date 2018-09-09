from slackclient import SlackClient
import time


class slackCommunication(object):
    def __init__(self):
        self.appName = "Beer2D2"
        self.token = "xoxb-174376887927-432114293189-mSijJZPEYW1hDLmI90opz3VA" #xoxb-431254460803-433050929142-igKpJF2877zevLNO9o5Omuyc
        self.sc = SlackClient(self.token)

    def slackConnect(self):
        return self.sc.rtm_connect()

    def slackReadRTM(self):
        return(self.sc.rtm_read())  # read all data from the RTM websocket

    def writeToSlack(self, channel, message):
        return self.sc.api_call("chat.postMessage", channel = channel, text = message, as_user = True)

    def getBotID(self, botusername):
       api_call = self.sc.api_call("users.list")
       users = api_call["members"]
       for user in users:
           if 'name' in user and botusername in user.get('name') and not user.get('deleted'):
              return user.get('id')
