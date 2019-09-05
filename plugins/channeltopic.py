import logging
from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, respond_to, process
import re

#logger = logging.getLogger(__name__)
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

    @respond_to(r'^add (?P<topic_string>\D+|\d+|me)')
    def topics(self, msg, topic_string):
        if topic_string == 'me':
            add_me_topic = msg.getTopic(global_event['channel']) + " " + msg.sender.name
            msg.setTopic(add_me_topic, global_event['channel'])
        else:
            msg.setTopic(topic_string, global_event['channel'])

    @respond_to(r'^rm (?P<remove_me>me)')
    def remove(self, msg, remove_me):
        if remove_me == 'me':
            rm_me_topic = msg.getTopic(global_event['channel'])
            rm_me_user = msg.sender.name
            remove_me_topic = rm_me_topic.replace(rm_me_user, '')
            remove_me_topic2 = remove_me_topic.strip()
            msg.setTopic(remove_me_topic2, global_event['channel'])
        else:
            pass

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
            try:
                msg.say(eval(pinging_string))
            except:
                msg.say("No valid users to ping...")
