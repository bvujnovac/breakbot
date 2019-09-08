#import logging
from datetime import datetime, timedelta
from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, respond_to, process
from slackclient import SlackClient
#from apscheduler.schedulers.background import BackgroundScheduler
from machine.singletons import Slack, Scheduler
import re

def getTime(t):
    return t[:2] + ':' + t[2:]

class LunchSetPlugin(MachineBasePlugin):
    @process(slack_event_type='message')
    def process_event(self, event):
        global global_event
        global_event = {}
        global_event['channel'] = event['channel']

    @respond_to(r'^lunch (?P<lunch_string>\d+|list|rm)')
    def topics(self, msg, topic_string):
        if topic_string == 'list':
            pass
        elif topic_string == 'rm':
            pass
        else:
            pass

    @respond_to(r'^set')
    def topics(self, msg):
#        slack_token = "xoxb-348044257717-722753499424-phV8z3ETVFF0px9fwdaL9UqH"
#        sc = SlackClient(slack_token)
#        catch = ""
#        try:
#        catch = sc.api_call("chat.scheduledMessages.list")
#        except:
#            pass
#        print(catch)
        in_300_sec = datetime.now() + timedelta(seconds=300)
        in_600_sec = datetime.now() + timedelta(seconds=600)
        lunch = msg.sender.name + "_lunch"
        lunchremind = msg.sender.name + "_lunchremind"
        msg.reply_dm_scheduled(in_300_sec, "A Delayed Hello!", lunch)
        msg.reply_dm_scheduled(in_600_sec, "A much more Delayed Hello!", lunchremind)

    @respond_to(r'^get')
    def topics2(self, msg):
        test = Scheduler.get_instance().get_jobs()
        print('----')
        dict = {}
        dict[msg.sender.name] = {}
        for x in test:
            dict[msg.sender.name][x.name] = {}
            dict[msg.sender.name][x.name]['id'] = x.id
            dict[msg.sender.name][x.name]['runtime'] = datetime.strftime(x.next_run_time, "%Y-%m-%d %H:%M:%S")
        print(dict)
        print('........')
        print(dict.get(msg.sender.name).get(msg.sender.name + "_lunch"))
        #print(Scheduler.get_instance().get_job(x.id))
        print('----')
        print("===============")

    @respond_to(r'^lunch (?P<lunch_time>\d+|rm)')
    def lunch(self, msg, lunch_time):
        if lunch_time == 'rm':
            print("lunch rm was asked by: " + msg.sender.name)
        else:
            requested_lunch = datetime.strptime(lunch_time,"%H%M").strftime("%H:%M")
            hour = datetime.strptime(lunch_time,"%H%M").strftime("%H")
            minute = datetime.strptime(lunch_time,"%H%M").strftime("%M")
            current_time = datetime.now()
            current_hour = current_time.strftime("%H")
            if hour < current_hour:
                now = datetime.now() + timedelta(days=1)
            else:
                now = datetime.now()
            #date_time = now.strftime("%Y-%m-%d, %H:%M:%S")
            lunch = now.strftime("%Y-%m-%d " + requested_lunch + ":00")
            lunch_reminder = datetime.strptime(lunch, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=15)
            print(lunch)
            print(lunch_reminder)
