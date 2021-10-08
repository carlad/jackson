# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from pattern.text.en import singularize
from typing import Any, Dict, List, Text
import requests
import yaml


class ActionSubmitQuery(Action):
    """Format keywords and submits query to black history api."""

    def name(self) -> Text:
        """Name the action."""
        return 'action_submit_query'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        """Normalize keywords and make request."""
        #  retrieve keywords slot value and normalize
        keywords = tracker.get_slot('keyword')
        query_string = '%20'.join([singularize(keyword) for keyword in keywords]) # noqa

        #  retrieve black history api key
        with open('./bha_credentials.yml', 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            key = cfg['credentials']['API_KEY']

        headers = {'x-api-key': key}

        #  look for results using all the keywords
        response = requests.get(
                    "https://rest.blackhistoryapi.io/fact/search/{}"
                    .format(query_string),
                    headers=headers).json()

        if response['TotalResults'] == 0:
            dispatcher.utter_message(
                """Sorry, I didn't find anything for: {}. Try using different keywords or names.""" # noqa
                .format(' '.join(keywords)))
            return

        else:
            texts = ''
            for i in response['Results']:
                texts += i['text'] + '\n\n'

        dispatcher.utter_message(texts)  # send the response back to the user
        return [SlotSet('keyword', 'none')]
