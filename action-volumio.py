#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
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

    @staticmethod
    def get_int_of_word(word):
        wordlist = ["null", "eins", "zwei", "drei", "view", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf",
                    "zwölf", "deizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn",
                    "zwanzig", "ein und zwanzig", "zwei und zwanzig", "drei und zwanzig", "vier und zwanzig",
                    "fünf und zwanzig", "sechs und zwanzig", "sieben und zwanzig", "acht und zwanzig",
                    "neun und zwanzig", "dreißig", "ein und dreißig", "zwei und dreißig", "drei und dreißig",
                    "vier und dreißig", "fünf und dreißig", "sechs und dreißig", "sieben und dreißig",
                    "acht und dreißig", "neun und dreißig", "vierzig", "ein und vierzig", "zwei und vierzig",
                    "drei und vierzig", "vier und vierzig", "fünf und vierzig", "sechs und vierzig",
                    "sieben und vierzig", "acht und vierzig", "neun und vierzig", "fünfzig", "ein und fünfzig",
                    "zwei und fünfzig", "drei und fünfzig", "vier und fünfzig", "fünf und fünfzig", "sechs und fünfzig",
                    "sieben und fünfzig", "acht und fünfzig", "neun und fünfzig", "sechzig", "ein und sechzig",
                    "zwei und sechzig", "drei und sechzig", "vier und sechzig", "fünf und sechzig", "sechs und sechzig",
                    "sieben und sechzig", "acht und sechzig", "neun und sechzig", "siebzig", "ein und siebzig",
                    "zwei und siebzig", "drei und siebzig", "vier und siebzig", "fünf und siebzig", "sechs und siebzig",
                    "sieben und siebzig", "acht und siebzig", "neun und siebzig", "achtzig", "ein und achtzig",
                    "zwei und achtzig", "drei und achtzig", "vier und achtzig", "fünf und achtzig", "sechs und achtzig",
                    "sieben und achtzig", "acht und achtzig", "neun und achtzig", "neunzig", "ein und neunzig",
                    "zwei und neunzig", "drei und neunzig", "vier und neunzig", "fünf und neunzig", "sechs und neunzig",
                    "sieben und neunzig", "acht und neunzig", "neun und neunzig", "einhundert"]

        if word in wordlist:
            return wordlist.index(word)

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
            hermes.publish_start_session_notification(intent_message.site_id,
                                                      "Ok, ich spiele die vorherige Wiedergabe.", "")

    def intent_next_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        response = requests.get(self.base_api_url + "next")
        responsejson = response.json()

        if responsejson["response"] == "next Success":
            # answer success
            hermes.publish_start_session_notification(intent_message.site_id, "Ok, ich spiele die nächste Wiedergabe.",
                                                      "")

    def intent_volume_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        #volumenumber = self.get_int_of_word(intent_message.slots.volume)

        # action code goes here...
        #if volumenumber is not None:
        if intent_message.slots.volume is not None:
            #response = requests.get(self.base_api_url + "volume&volume={0}".format(volumenumber))
            response = requests.get(self.base_api_url + "volume&volume={}".format(int(intent_message.slots.volume.first().value)))
            responsejson = response.json()

            if responsejson["response"] == "volume Success":
                # answer success
                hermes.publish_start_session_notification(intent_message.site_id,
                                                          "Ok, Lautstärke ist jetzt bei {}.".format(
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

    # --> Register callback function and start MQTT
    def start_blocking(self):
        mqtt_addr = "{}:{}".format(self.config["global"]["mqtt_ip_addr"], self.config["global"]["mqtt_port"])

        mqtt_opts = MqttOptions(username=self.config["secret"]["mqtt_user"], password=self.config["secret"]["mqtt_pw"],
                                broker_address=mqtt_addr)
        with Hermes(mqtt_options=mqtt_opts) as h:
            h.subscribe_intents(self.master_intent_callback).start()


if __name__ == "__main__":
    Volumio()
