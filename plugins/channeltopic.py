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

    @respond_to(r'^(?P<agent_alert>chats|seconds|tickets|ping)')
    def listen_to_agent_alert(self, msg, agent_alert):
        print(global_event['channel'])
        logger.debug("Used keyword: %s", agent_alert)
        get_chanel_topic = msg.getTopic(global_event['channel'])

        '''
        try:
            get_chanel_topic['channel']['topic']['value']
        except:
            get_agents = get_chanel_topic['group']['topic']['value']
        else:
            get_agents = get_chanel_topic['channel']['topic']['value']
        '''

        get_agents = get_chanel_topic
        print(get_agents)
        logger.debug("Recieved all: %s", get_agents)
        searching = re.compile('(?:chats:)(.*)(?:seconds:)(.*)(?:tickets:)(.*)|(?:chats:)(.*)(?:seconds:)(.*)|(?:chats:)(.*)(?:tickets:)(.*)|(?:seconds:)(.*)(?:tickets:)(.*)|(?:chats:)(.*)|(?:seconds:)(.*)|(?:tickets:)(.*)')
        result = searching.search(get_agents)
        if result:
            if result.group(1) is not None:
                chats = result.group(1)
            if result.group(2) is not None:
                seconds = result.group(2)
            if result.group(3) is not None:
                tickets = result.group(3)
            if result.group(4) is not None:
                chats = result.group(4)
            if result.group(5) is not None:
                seconds = result.group(5)
            if result.group(6) is not None:
                chats = result.group(6)
            if result.group(7) is not None:
                tickets = result.group(7)
            if result.group(8) is not None:
                seconds = result.group(8)
            if result.group(9) is not None:
                tickets = result.group(9)
            if result.group(10) is not None:
                chats = result.group(10)
            if result.group(11) is not None:
                seconds = result.group(11)
            if result.group(12) is not None:
                tickets = result.group(12)

        tickets_string = ""
        if agent_alert == 'tickets':
            try:
                tickets
            except:
                msg.say('There are no admins on tickets..hmmm')
            else:
                tickets_list = Convert(tickets)
                tickets_list = list(filter(None, tickets_list))
                for user in tickets_list:
                    tickets_string += "self.at('" + user + "') + "
                tickets_string = tickets_string.strip(' +')
                msg.say(eval(tickets_string))


        seconds_string = ""
        if agent_alert == 'seconds':
            try:
                seconds
            except:
                msg.say('There are no seconds..hmmm')
            else:
                seconds_list = Convert(seconds)
                seconds_list = list(filter(None, seconds_list))
                for user in seconds_list:
                    seconds_string += "self.at('" + user + "') + "
                seconds_string = seconds_string.strip(' +')
                msg.say(eval(seconds_string))

        chats_string = ""
        if agent_alert == 'chats':
            try:
                chats
            except:
                msg.say('There are no chatters..hmmm')
            else:
                chats_list = Convert(chats)
                chats_list = list(filter(None, chats_list))
                for user in chats_list:
                    chats_string += "self.at('" + user + "') + "
                chats_string = chats_string.strip(' +')
                msg.say(eval(chats_string))

#pinging part
        if agent_alert == 'ping':
            ping_string = ""
            try:
                chats
            except:
                print ("chats are not defined")
            else:
                chats_list = Convert(chats)
                chats_list = list(filter(None, chats_list))
                for user in chats_list:
                    chats_string += "self.at('" + user + "') + "
                chats_string = chats_string.strip(' +')

            try:
                seconds
            except:
                print ("seconds are not defined")
            else:
                seconds_list = Convert(seconds)
                seconds_list = list(filter(None, seconds_list))
                for user in seconds_list:
                    seconds_string += "self.at('" + user + "') + "
                seconds_string = seconds_string.strip(' +')

            try:
                tickets
            except:
                print ("tickets are not defined")
            else:
                tickets_list = Convert(tickets)
                tickets_list = list(filter(None, tickets_list))
                for user in tickets_list:
                    tickets_string += "self.at('" + user + "') + "
                tickets_string = tickets_string.strip(' +')

            ping_string = chats_string + " + " + seconds_string + " + " + tickets_string
            ping_string = ping_string.strip('+ ')
            logger.debug("Check ping: %s", ping_string)
            msg.say(eval(ping_string))
