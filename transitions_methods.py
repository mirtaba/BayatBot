import telegram
import database_manager as db


class Methods:
    def welcome(self, update):
        custom_keyboard = [['اضافه کردن کلاس'], ['اضافه کردن استاد'], ['درخواست کلاس']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text(text='به بیات بات خوش آمدید!' + '\n' + 'بر روی یکی از کلید های زیر کلید کنید:',
                                  reply_markup=reply_markup)

    def add_class_msg(self, update):
        update.message.reply_text(
            'برای اضافه کردن کلاس از دستور زیر استفاده کنید:\nشماره‌کلاس  ظرفیت‌کلاس  توضیح‌کلاس\n* توضیح کلاس اختیاری است\n\nبرای مثال:\n103 30 کلاس دارای پیریز برق نیست');

    def class_added(self, update, c_number, cap, des):
        update.message.reply_text('کلاس با مشخصات زیر اضافه شد:\n'
                                  'شماره کلاس: ' + c_number + '\n'
                                                              'ظرفیت کلاس: ' + cap + '\n'
                                                                                     'توضیحات:\n'
                                  + str(des))

    def add_teacher_msg(self, update):
        update.message.reply_text(
            'لطفا نام و نام‌خانوادگی استاد مورد نظر را وارد نمایید\n'
            'لطفا در ورودی خود فقط یک فاصله بین اسم و فامیل استفاده کنید و بقیه فاصله‌ها را با نیم‌فاصله مشخص فرمایید'
        )

    def teacher_added(self, update, name, familyName):
        db.add_teacher(name, familyName)
        update.message.reply_text(
            'استاد با نام %s و نام‌خانوادگی %s به سیستم افزوده شد.' % (name, familyName)
        )
