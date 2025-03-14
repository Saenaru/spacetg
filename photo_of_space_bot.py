import os
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackContext
from environs import Env


def post_to_channel(update: Update, context: CallbackContext) -> None:
    channel_id = "@photo_of_space"
    image_directory = "images"
    images = os.listdir(image_directory)
    if not images:
        context.bot.send_message(chat_id=update.effective_chat.id, text="В папке нет изображений.")
        return
    image_path = os.path.join(image_directory, images[0])
    try:
        with open(image_path, 'rb') as photo:
            context.bot.send_photo(chat_id=channel_id, photo=photo)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Не удалось отправить изображение: {e}")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я ваш бот. Используйте команду /post для отправки изображения в канал.')



def main():
    env = Env()
    env.read_env("token.env")
    token = env.str("TG_SPACE_TOKEN")
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("post", post_to_channel))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()