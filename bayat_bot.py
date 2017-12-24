from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram.update import Update

import database_manager
from FSM import FSM

temp_map = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    # inserts new user to database (if not exist) and sets initial state to 'initial'
    state = database_manager.get_user_state(update.message.chat.id)
    if state != 'initial':
        database_manager.set_user_state(update.message.chat.id, 'initial')
    fsm = FSM('initial')
    fsm.machine.start(update)
    database_manager.set_user_state(update.message.chat.id, fsm.machine.state)


def help(bot, update):
    update.message.reply_text('Help!')


def message_handler(bot, update):
    state = database_manager.get_user_state(update.message.chat.id)
    fsm = FSM(state)
    print("state before is: " + fsm.machine.state)
    if update.message.text == 'بازشگت به منو اولیه':
        start(bot, update)
    elif update.message.text == 'اضافه کردن کلاس':
        fsm.machine.add_class(update)
        print("state after is: " + fsm.machine.state)
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    elif update.message.text == 'اضافه کردن استاد':
        fsm.machine.add_teacher(update)
        print("state after is: " + fsm.machine.state)
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    elif update.message.text == 'درخواست کلاس':
        fsm.machine.get_i(update) # go to state for getting instractor
        print("state after is: " + fsm.machine.state)
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    elif fsm.machine.state == 'new_class':
        parts = update.message.text.split(' ')
        class_description = ''
        for word in parts[2:]:
            class_description += word + ' '
        database_manager.add_class(parts[0], parts[1], class_description)
        fsm.machine.add_class_finished(update, parts[0], parts[1], class_description)
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    elif fsm.machine.state == 'new_teacher':
        parts = update.message.text.split(' ')
        database_manager.add_teacher(parts[0], parts[1])
        fsm.machine.add_teacher_finished(update, parts[0], parts[1], )
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    elif fsm.machine.state == 'get_class_i':
        temp_map[update.message.chat.id] = [update.message.text]
        fsm.machine.get_w(update)
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    elif fsm.machine.state == 'get_class_w':
        temp_map[update.message.chat.id].append(update.message.text)
        fsm.machine.get_t(update)
        database_manager.set_user_state(update.message.chat.id, fsm.machine.state)

    elif fsm.machine.state == 'get_class_t':
        temp_map[update.message.chat.id].append(update.message.text)

        taken_class = database_manager.find_and_insert_class(temp_map[update.message.chat.id])

        fsm.machine.class_got(update, taken_class,
                              temp_map[update.message.chat.id][0],
                              temp_map[update.message.chat.id][1],
                              temp_map[update.message.chat.id][2],
                              )

        del temp_map[update.message.chat.id]
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
