#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from word2number import w2n
from hermes_python.ontology import *
from hermes_python.ffi.utils import MqttOptions
import io
import requests

CONFIG_INI = "config.ini"


class Volumio(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except:
            self.config = None

        self.base_api_url = "http://{0}:{1}/api/v1/commands/?cmd=".format(self.config["global"]["host"],
                                                                          self.config["global"]["port"])

        # start listening to MQTT
        self.start_blocking()

    # --> Sub callback function, one per intent
    def intent_play_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        response = requests.get(self.base_api_url + "play")
        responsejson = response.json()

        if responsejson["response"] == "play Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich starte die Wiedergabe.", "")

    def intent_stop_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        response = requests.get(self.base_api_url + "stop")
        responsejson = response.json()

        if responsejson["response"] == "stop Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich stope die Wiedergabe.", "")

    def intent_pause_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        response = requests.get(self.base_api_url + "pause")
        responsejson = response.json()

        if responsejson["response"] == "pause Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich pausiere die Wiedergabe.", "")

    def intent_prev_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        response = requests.get(self.base_api_url + "prev")
        responsejson = response.json()

        if responsejson["response"] == "prev Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich spiele die vorherige Wiedergabe.", "")

    def intent_next_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        response = requests.get(self.base_api_url + "next")
        responsejson = response.json()

        if responsejson["response"] == "next Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich spiele die nächste Wiedergabe.", "")

    def intent_volume_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        volumeNumber = w2n.word_to_num(intent_message.slots.volume)

        # action code goes here...
        if isinstance(volumeNumber, int):
            response = requests.get(self.base_api_url + "volume&volume={0}".format())
            responsejson = response.json()

            if responsejson["response"] == "volume Success":
                # answer success
                hermes.publish_start_session_notification(intent_message.site_id, "Ok, Lautstärke ist jetzt bei {0}.".format(intent_message.slots.volume), "")


    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self, hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == "Hodor:Play":
            self.intent_play_callback(hermes, intent_message)
        if coming_intent == "Hodor:Stop":
            self.intent_stop_callback(hermes, intent_message)
        if coming_intent == "Hodor:Pause":
            self.intent_pause_callback(hermes, intent_message)
        if coming_intent == "Hodor:Prev":
            self.intent_prev_callback(hermes, intent_message)
        if coming_intent == "Hodor:Next":
            self.intent_next_callback(hermes, intent_message)
        if coming_intent == "Hodor:Volume":
            self.intent_volume_callback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        mqtt_addr = "{}:{}".format(self.config["global"]["mqtt_ip_addr"], self.config["global"]["mqtt_port"])

        mqtt_opts = MqttOptions(username=self.config["secret"]["mqtt_user"], password=self.config["secret"]["mqtt_pw"],
                                broker_address=mqtt_addr)
        with Hermes(mqtt_options=mqtt_opts) as h:
            h.subscribe_intents(self.master_intent_callback).start()


if __name__ == "__main__":
    Volumio()
