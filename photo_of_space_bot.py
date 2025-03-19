import os
import random
import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from environs import Env


def post_to_channel(update: Update, context: CallbackContext, image_directory: str, channel_id: str) -> None:
    images = os.listdir(image_directory)

    if not images:
        context.bot.send_message(chat_id=update.effective_chat.id, text="В папке нет изображений.")
        return
    if not context.args:
        image_name = random.choice(images)
    else:
        image_name = context.args[0]
        if image_name not in images:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Файл {image_name} не найден.")
            return
    image_path = os.path.join(image_directory, image_name)
    with open(image_path, 'rb') as photo:
        context.bot.send_photo(chat_id=channel_id, photo=photo)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Фото успешно отправлено в канал!")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Привет! Я ваш бот. Используйте команду /post <имя_файла> для отправки изображения в канал. '
        'Без указания имени будет выбрано случайное изображение.'
    )


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    env = Env()
    env.read_env("token.env")
    try:
        token = env.str("TG_SPACE_TOKEN")
    except KeyError:
        logging.error("Токен не найден в переменных среды")
        return
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    image_directory = "images"
    channel_id = "@photo_of_space"
    def wrapped_post_to_channel(update: Update, context: CallbackContext) -> None:
        try:
            post_to_channel(update, context, image_directory, channel_id)
        except FileNotFoundError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Каталог не найден.")
        except IOError as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Не удалось открыть изображение: {e}")
            logging.error("Error opening photo: %s", e)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("post", wrapped_post_to_channel))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()