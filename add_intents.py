import json
import os

import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from google.api_core import exceptions


EXAMPLE_PATH = "data/intent_example.json"
QUESTIONS_PATH = "data/questions.json"


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    intents_client.create_intent(parent, intent)


def create_intents_from_file(path, project_id):
    with open(path, "r") as file:
        questions = json.load(file)
        for key, value in questions.items():
            display_name = key
            training_phrases_parts = value["questions"]
            message_text = value["answer"]
            message_texts = [message_text]
            try:
                create_intent(project_id, display_name, training_phrases_parts,
                              message_texts)
            except exceptions.InvalidArgument as error:
                print('Exceptions: {}'.format(error))  # TODO: заменить на логгинг
                pass


def main():

    load_dotenv()

    project_id = os.getenv("PROJECT_ID")
    create_intents_from_file(QUESTIONS_PATH, project_id)


if __name__ == '__main__':
    main()
