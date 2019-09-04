import logging
from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, respond_to, process
import re

logger = logging.getLogger(__name__)
def Convert(string):
    li = list(string.split(" "))
    return li
global_event = {}

class TopicSetPlugin(MachineBasePlugin):
    @process(slack_event_type='message')
    def process_event(self, event):
        global global_event
        global_event = {}
        global_event['channel'] = event['channel']

    @respond_to(r'^add (?P<topic_string>\D+|\d+)')
    def topics(self, msg, topic_string):
        msg.setTopic(topic_string, global_event['channel'])

class TopicReadPlugin(MachineBasePlugin):
    @process(slack_event_type='message')
    def process_event(self, event):
        global global_event
        global_event = {}
        global_event['channel'] = event['channel']

    @respond_to(r'^(?P<agent_alert>chats|ping)')
    def listen_to_agent_alert(self, msg, agent_alert):
        get_topic = msg.getTopic(global_event['channel'])
        userregex = re.compile(r'[a-zA-Z]+|<@[A-Z0-9]+>')
        topicUsers = userregex.findall(get_topic)
        if agent_alert == 'ping':
            ping_string = ""
            for tu in topicUsers:
                try:
                    allUsers = self.users.find(tu)
                    ping_string += allUsers.name +" "
                except:
                    pass
            ping_list = list(filter(None, Convert(ping_string)))
            pinging_string = ""
            for user in ping_list:
                pinging_string += "self.at('" + user + "') + "
            pinging_string = pinging_string.strip(' +')
            msg.say(eval(pinging_string))
