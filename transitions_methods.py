import telegram
import database_manager as db


class Methods:
    menu = [['اضافه کردن کلاس'], ['اضافه کردن استاد'], ['درخواست کلاس']]

    def welcome(self, update):
        reply_markup = telegram.ReplyKeyboardMarkup(self.menu)
        update.message.reply_text(text='به بیات بات خوش آمدید!' + '\n' + 'بر روی یکی از کلید های زیر کلیک کنید:',
                                  reply_markup=reply_markup)

    def add_class_msg(self, update):
        update.message.reply_text(
            'برای اضافه کردن کلاس از دستور زیر استفاده کنید:\nشماره‌کلاس  ظرفیت‌کلاس  توضیح‌کلاس\n* توضیح کلاس اختیاری است\n\nبرای مثال:\n103 30 کلاس دارای پیریز برق نیست',
            reply_markup=telegram.ReplyKeyboardMarkup([['بازشگت به منو اولیه']])
        )

    def class_added(self, update, c_number, cap, des):
        update.message.reply_text('کلاس با مشخصات زیر اضافه شد:\n'
                                  'شماره کلاس: ' + c_number + '\n'
                                                              'ظرفیت کلاس: ' + cap + '\n'
                                                                                     'توضیحات:\n' + str(des),
                                  reply_markup=telegram.ReplyKeyboardMarkup(self.menu)
                                  )

    def add_teacher_msg(self, update):
        update.message.reply_text(
            'لطفا نام و نام‌خانوادگی استاد مورد نظر را وارد نمایید\n'
            'لطفا در ورودی خود فقط یک فاصله بین اسم و فامیل استفاده کنید و بقیه فاصله‌ها را با نیم‌فاصله مشخص فرمایید',
            reply_markup=telegram.ReplyKeyboardMarkup([['بازشگت به منو اولیه']])
        )

    def teacher_added(self, update, name, familyName):
        update.message.reply_text(
            'استاد با نام %s و نام‌خانوادگی %s به سیستم افزوده شد.' % (name, familyName),
            reply_markup=telegram.ReplyKeyboardMarkup(self.menu)
        )

    def get_class_i_msg(self, update):

        teacher_keyboard = [['بازشگت به منو اولیه']]
        for teacher in db.get_teachers_list():
            teacher_keyboard.append([teacher])

        update.message.reply_text(
            'از بین موارد زیر استاد درس را انتخاب کنید: ',
            reply_markup=telegram.ReplyKeyboardMarkup(teacher_keyboard)
        )

    def get_class_w_msg(self, update):
        teacher_keyboard = [['بازشگت به منو اولیه'],
                            ['دوشنبه', 'یکشنبه', 'شنبه'],
                            ['پنجشنبه', 'چهارشنبه', 'سه‌شنبه']
                            ]

        update.message.reply_text(
            'از بین موارد زیر روز کلاس را انتخاب کنید: ',
            reply_markup=telegram.ReplyKeyboardMarkup(teacher_keyboard)
        )

    def get_class_t_msg(self, update):
        teacher_keyboard = [['بازشگت به منو اولیه'],
                            ['7:30 - 9'],
                            ['9 - 10:30'],
                            ['10:30 - 12'],
                            ['12 - 13'],
                            ['13 - 14'],
                            ['14 - 15:30'],
                            ]

        update.message.reply_text(
            'از بین موارد زیر زمان کلاس را انتخاب کنید: ',
            reply_markup=telegram.ReplyKeyboardMarkup(teacher_keyboard)
        )

    def get_class_finished(self, update, class_number, teacher, week, time):
        if class_number != -1:
            update.message.reply_text(
                'کلاس شماره ' +
                str(class_number) +
                ' برای ' + week + ' ها ' + 'ساعت ' + time +
                ' برای استاد ' +
                str(teacher) +
                ' رزرو شد.',
                reply_markup=telegram.ReplyKeyboardMarkup(self.menu)
            )
        else:
            update.message.reply_text(
                'در روز ' + week + 'ها ' + 'ساعت ' + time +
                ' کلاس خالی وجود ندارد. لطفا ساعت دیگری را امتحان کنید.',
                reply_markup=telegram.ReplyKeyboardMarkup(self.menu)
            )
