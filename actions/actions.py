"""Custom actions used to run custom Python code."""

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from pattern.text.en import singularize
from typing import Any, Dict, List, Text
import requests
import bha_credentials


class ActionSubmitQuery(Action):
    """Format keywords and submits query to black history api."""

    def name(self) -> Text:
        """Name the action."""
        return 'action_submit_query'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        """Normalize keywords and make request."""
        #  retrieve keywords slot value
        keywords = tracker.get_slot('keywords')
        print(keywords)
        print(keywords[0])

        # return if no keyword entities are detected
        if keywords is None:
            dispatcher.utter_message(
                "Sorry, I wasn't able to understand your request. Try using different keywords or names.") # noqa

        else:
            # set headers
            headers = {'x-api-key': bha_credentials.API_KEY}

            # find a random fact
            if keywords[0] == 'random' or keywords[0] == 'randomly':
                response = requests.get(
                        "https://rest.blackhistoryapi.io/fact/random",
                        headers=headers).json()

                text = response['Results'][0]['text']

                dispatcher.utter_message(
                        "Here's the random fact I found for you: \n{}.".format(text)) # noqa

            else:
                # normalize keywords
                query_string = '%20'.join([singularize(keyword) for keyword in keywords]) # noqa

                #  look for results using all the keywords
                response = requests.get(
                            "https://rest.blackhistoryapi.io/fact/search/{}"
                            .format(query_string),
                            headers=headers).json()

                total_results = response['TotalResults']

                if total_results == 0:
                    dispatcher.utter_message(
                        "Sorry, I didn't find anything for: {}. Try using different keywords or names." # noqa
                        .format(' '.join(keywords)))

                else:
                    fact_string = 'fact' if total_results == 1 else 'facts'
                    texts = 'I found {} {}:\n'.format(total_results, fact_string) # noqa
                    for i in response['Results']:
                        texts += '{}\n'.format(i['text'])

                dispatcher.utter_message(texts)

        return [SlotSet('keywords', 'none')]
