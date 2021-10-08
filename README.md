## Description

Jackson is a chatbot that helps find historical facts about black people. It is named after Mary W. Jackson, the first African American female engineer at NASA.

Jackson is built with [Rasa](https://github.com/RasaHQ/rasa), the open source machine learning framework that automates text-and voice-based conversations. Jackson uses the [Black History API](https://blackhistoryapi.com/), which documents achievements and facts about black people, past and present. 

Jackson uses a simple keyword search.

## Dependencies

Python 3.8.6

Jackson requires [rasa-sdk](https://github.com/RasaHQ/rasa-sdk) to run the custom search action:
```
pip install rasa-sdk
```

and [Pattern](https://github.com/clips/pattern) to singularize keywords:
```
pip install pattern
```

## To run

To enable api calls to the Black History API you will need to [sign-up](https://blackhistoryapi.com/#signUp) for an api key from the Black History API, then add this key to a new file in the home directory named `bha_credentials.yml`

```
credentials:
    API_KEY: XXXXXXXXXXXX
```

To talk to Jackson on the command line, start the Rasa Action Server in one terminal window: 
```
rasa run actions
```

Then in a new terminal window run `rasa shell`, and follow the prompts.

## Further Help

Please refer to the [Rasa Docs](https://rasa.com/docs/rasa/) for more information about Rasa Open Source.
