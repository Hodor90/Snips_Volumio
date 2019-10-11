#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from hermes_python.ffi.utils import MqttOptions
import io
import requests
from unittest import mock

CONFIG_INI = "config.ini"


class Volumio(object):

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

        responsejson = self.makeVolumioApiCall("play")

        if responsejson["response"] == "play Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich starte die Wiedergabe.", "")

    def intent_stop_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        responsejson = self.makeVolumioApiCall("stop")

        if responsejson["response"] == "stop Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich stope die Wiedergabe.", "")

    def intent_pause_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        responsejson = self.makeVolumioApiCall("pause")

        if responsejson["response"] == "pause Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich pausiere die Wiedergabe.", "")

    def intent_prev_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        responsejson = self.makeVolumioApiCall("prev")

        if responsejson["response"] == "prev Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id,
                                                      "Ok, ich spiele die vorherige Wiedergabe.", "")

    def intent_next_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        responsejson = self.makeVolumioApiCall("next")

        if responsejson["response"] == "next Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich spiele die nächste Wiedergabe.",
                                                      "")

    def intent_volume_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        #if volumenumber is not None:
        if intent_message.slots.volume is not None:
            #"volume&volume={0}".format(volumenumber)
            responsejson = self.makeVolumioApiCall("volume&volume={}".format(int(intent_message.slots.volume.first().value)))

            if responsejson["response"] == "volume Success":
                # answer success
                hermes.publish_start_session_notification(intent_message.site_id,
                                                          "Ok, Lautstärke ist jetzt bei {}".format(
                                                              int(intent_message.slots.volume.first().value)), "")

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

    def makeVolumioApiCall(self, method):
        # action code goes here...
        response = requests.get(self.base_api_url + method)
        return response.json()

    # --> Register callback function and start MQTT
    def start_blocking(self):
        mqtt_addr = "{}:{}".format(self.config["global"]["mqtt_ip_addr"], self.config["global"]["mqtt_port"])

        mqtt_opts = MqttOptions(username=self.config["secret"]["mqtt_user"], password=self.config["secret"]["mqtt_pw"],
                                broker_address=mqtt_addr)
        with Hermes(mqtt_options=mqtt_opts) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Volumio()
