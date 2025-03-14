from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackContext
from functools import wraps
from environs import Env

def post_to_channel(update: Update, context: CallbackContext) -> None:
    channel_id = "@photo_of_space"
    context.bot.send_message(chat_id=channel_id, text="Привет, канал! Это сообщение от вашего бота.")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я ваш бот. Используйте команду /post для отправки сообщения в канал.')

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