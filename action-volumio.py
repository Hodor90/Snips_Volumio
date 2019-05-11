#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from hermes_python.ffi.utils import MqttOptions
import io
import requests

CONFIG_INI = "config.ini"


class Volumio():
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except:
            self.config = None

        self.base_api_url = "http://{0}:{1}/api/v1/commands/?cmd=".format(self.config['global']['host'],
                                                                          self.config['global']['port'])

        # start listening to MQTT
        self.start_blocking()

    # --> Sub callback function, one per intent
    def intent_play_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "Play")

        # action code goes here...
        requests.get(self.base_api_url + "play")

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Action1 has been done", "")

    def intent_stop_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "Stop")

        # action code goes here...
        requests.get(self.base_api_url + "stop")

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Action2 has been done", "")

    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self, hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'Play':
            self.intent_play_callback(hermes, intent_message)
        if coming_intent == 'Stop':
            self.intent_stop_callback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        mqtt_addr = "{}:{}".format(self.config['global']['mqtt_ip_addr'], self.config['global']['mqtt_port'])

        mqtt_opts = MqttOptions(username=self.config['secret']['mqtt_user'], password=self.config['secret']['mqtt_pw'],
                                broker_address=mqtt_addr)
        with Hermes(mqtt_options=mqtt_opts) as h:
            h.subscribe_intents(self.master_intent_callback).start()


if __name__ == "__main__":
    Volumio()
