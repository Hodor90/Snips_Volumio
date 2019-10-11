from action_volumio import Volumio
import unittest
from unittest.mock import Mock
from unittest.mock import patch
from unittest import mock
from hermes_python.ontology.dialogue import IntentMessage
from hermes_python.ontology.dialogue import IntentClassifierResult
from hermes_python.ontology.dialogue import SlotMap
from hermes_python.ontology.dialogue.slot import CustomValue
from hermes_python.ontology.dialogue.slot import SlotValue
from hermes_python.ontology.dialogue.slot import NluSlot
from hermes_python.ontology.dialogue.slot import SlotsList

class Test_TestIncrementDecrement(unittest.TestCase):

    @patch('action_volumio.Volumio.start_blocking', return_value = "")
    @patch('action_volumio.Volumio.makeVolumioApiCall', return_value = {"response" : "play Success"})
    def test_play(self, start_blocking, makeVolumioApiCall):
        volumio = Volumio()
        
        hermes = Mock()
        intent_message = IntentMessage("testId", [], "testSiteId", "starte wiedergabe", 
                    IntentClassifierResult("Hodor:Play", 1), [])
                        
        volumio.master_intent_callback(hermes, intent_message)
    
        hermes.publish_end_session.assert_called_once_with("testId", "")
        hermes.publish_start_session_notification.assert_called_once_with("testSiteId", "Ok, ich starte die Wiedergabe.", "")
 
    @patch('action_volumio.Volumio.start_blocking', return_value = "")
    @patch('action_volumio.Volumio.makeVolumioApiCall', return_value = {"response" : "stop Success"})
    def test_stop(self, start_blocking, makeVolumioApiCall):
        volumio = Volumio()
        
        hermes = Mock()
        intent_message = IntentMessage("testId", [], "testSiteId", "stope wiedergabe", 
                    IntentClassifierResult("Hodor:Stop", 1), [])
        volumio.master_intent_callback(hermes, intent_message)
    
        hermes.publish_end_session.assert_called_once_with("testId", "")
        hermes.publish_start_session_notification.assert_called_once_with("testSiteId", "Ok, ich stope die Wiedergabe.", "")


    @patch('action_volumio.Volumio.start_blocking', return_value = "")
    @patch('action_volumio.Volumio.makeVolumioApiCall', return_value = {"response" : "pause Success"})
    def test_pause(self, start_blocking, makeVolumioApiCall):
        volumio = Volumio()
        
        hermes = Mock()
        intent_message = IntentMessage("testId", [], "testSiteId", "halte wiedergabe an", 
                    IntentClassifierResult("Hodor:Pause", 0.9198287), [])
        volumio.master_intent_callback(hermes, intent_message)
    
        hermes.publish_end_session.assert_called_once_with("testId", "")
        hermes.publish_start_session_notification.assert_called_once_with("testSiteId", "Ok, ich pausiere die Wiedergabe.", "")

    @patch('action_volumio.Volumio.start_blocking', return_value = "")
    @patch('action_volumio.Volumio.makeVolumioApiCall', return_value = {"response" : "prev Success"})
    def test_prev(self, start_blocking, makeVolumioApiCall):
        volumio = Volumio()
        
        hermes = Mock()
        intent_message = IntentMessage("testId", [], "testSiteId", "spiele vorherige wiedergabe", 
                    IntentClassifierResult("Hodor:Prev", 0.9772446), [])
        volumio.master_intent_callback(hermes, intent_message)
    
        hermes.publish_end_session.assert_called_once_with("testId", "")
        hermes.publish_start_session_notification.assert_called_once_with("testSiteId", "Ok, ich spiele die vorherige Wiedergabe.", "")

    @patch('action_volumio.Volumio.start_blocking', return_value = "")
    @patch('action_volumio.Volumio.makeVolumioApiCall', return_value = {"response" : "next Success"})
    def test_next(self, start_blocking, makeVolumioApiCall):
     
        volumio = Volumio()
        
        hermes = Mock()
        intent_message = IntentMessage("testId", [], "testSiteId", "next", 
                    IntentClassifierResult("Hodor:Next", 1), [])                                                                                       
        volumio.master_intent_callback(hermes, intent_message)
    
        hermes.publish_end_session.assert_called_once_with("testId", "")
        hermes.publish_start_session_notification.assert_called_once_with("testSiteId", "Ok, ich spiele die nächste Wiedergabe.", "")

    @patch('action_volumio.Volumio.start_blocking', return_value = "")
    @patch('action_volumio.Volumio.makeVolumioApiCall', return_value = {"response" : "volume Success"})
    def test_volume(self, start_blocking, makeVolumioApiCall):
     
        volumio = Volumio()
        
        hermes = Mock()

        custom_slot_value = CustomValue("50")
        slot_value = SlotValue(1, custom_slot_value)
        nlu_slot = NluSlot(1, slot_value, "fünfzig", "volume", "volume", 15, 22)
        slots_list = SlotsList()
        slots_list.append(nlu_slot)
        
        slot_map = dict([(nlu_slot.slot_name, slots_list)])
        slots = SlotMap(slot_map)

        intent_message = IntentMessage("testId", [], "testSiteId", "lautstärke auf fünfzig", 
                    IntentClassifierResult("Hodor:Volume", 1), slots)

        volumio.master_intent_callback(hermes, intent_message)
    
        hermes.publish_end_session.assert_called_once_with("testId", "")
        hermes.publish_start_session_notification.assert_called_once_with("testSiteId", "Ok, Lautstärke ist jetzt bei 50", "")
    
if __name__ == '__main__':
    unittest.main()