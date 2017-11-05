from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram.update import Update

import database_manager
from FSM import FSM

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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

    elif fsm.machine.state == 'new_class':
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

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, message_handler))

    dp.add_error_handler(error)

    updater.start_polling()
    print("bot started.")

    updater.idle()

if __name__ == '__main__':
    main()
