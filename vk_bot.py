import os
import random

import dialogflow_v2 as dialogflow
import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll


def send_reply(event, vk_auth):
    project_id = os.getenv("PROJECT_ID")
    session_id = random.getrandbits(128)
    language_code = "ru-RU"

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    user_text = event.text
    text_input = dialogflow.types.TextInput(
        text=user_text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    if response.query_result.intent.is_fallback:
        return

    vk_auth.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
        random_id=session_id)


def main():
    load_dotenv()

    vk_group_api_key = os.getenv("VK_GROUP_API_KEY")
    vk_session = vk_api.VkApi(token=vk_group_api_key)
    vk_auth = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_reply(event, vk_auth)


if __name__ == "__main__":
    main()
