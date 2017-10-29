from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import psycopg2
from telegram.update import Update

import database_manager
from FSM import FSM

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    # inserts new user to database (if not exist) and sets initial state to 'initial'
    state = database_manager.get_user_state(update.message.chat.id)
    fsm = FSM(state)
    print("state before is: " + fsm.machine.state)
    fsm.machine.start(update)
    print("state after is: " + fsm.machine.state)
    database_manager.set_user_state(update.message.chat.id, fsm.machine.state)


def help(bot, update):
    update.message.reply_text('Help!')


def message_handler(bot, update):
    state = database_manager.get_user_state(update.message.chat.id)
    fsm = FSM(state)
    print("state before is: " + fsm.machine.state)
    if update.message.text == 'اضافه کردن کلاس':
        fsm.machine.add_class(update)
        print("state after is: " + fsm.machine.state)
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    else:
        parts = update.message.text.split(' ')
        print('FFFFFFFFFuuuuuuuuuuucccccccckkkkk: ')
        for p in parts:
            print(p)
        database_manager.add_class(parts[0], parts[1], parts[2:])
        fsm.machine.add_class_finished(update, parts[0], parts[1], parts[2:])
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)




        # update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = '442623399:AAGmotTuyXZ26Il29ysq0O0xRBQ9_PEoDhY'
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print("bot started.")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
