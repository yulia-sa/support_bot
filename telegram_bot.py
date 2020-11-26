import logging
import os

import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def error(update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def detect_intent_text(bot, update):
    project_id = os.getenv("PROJECT_ID")
    session_id = update.message.chat_id
    language_code = "ru-RU"

    user_text = update.message.text

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=user_text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    bot.send_message(chat_id=update.message.chat_id, text=response.query_result.fulfillment_text)


def main():
    load_dotenv()

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    # google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(telegram_bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, detect_intent_text))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
