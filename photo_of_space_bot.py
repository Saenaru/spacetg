import os
import random
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from environs import Env

env = Env()
env.read_env("token.env")


def post_to_channel(update: Update, context: CallbackContext) -> None:
    channel_id = env.str("TG_CHANEL_NAME")
    image_directory = "images"
    try:
        images = os.listdir(image_directory)
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Каталог не найден.")
        return
    if not images:
        context.bot.send_message(chat_id=update.effective_chat.id, text="В папке нет изображений.")
        return
    if context.args:
        image_name = context.args[0]
        image_path = os.path.join(image_directory, image_name)
        if image_name not in images:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Файл {image_name} не найден.")
            return
    else:
        image_path = os.path.join(image_directory, random.choice(images))
    try:
        with open(image_path, 'rb') as photo:
            context.bot.send_photo(chat_id=channel_id, photo=photo)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Фото успешно отправлено в канал!")
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Не удалось отправить изображение: {e}")
        logging.error("Error sending photo: %s", e)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я ваш бот. Используйте команду /post <имя_файла> для отправки изображения в канал. Без указания имени будет выбрано случайное изображение.')


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    token = env.str("TG_SPACE_TOKEN")
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("post", post_to_channel))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
