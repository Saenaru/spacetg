import os
import random
import time
import argparse
from telegram import Bot
from environs import Env


def post_photo(bot, channel_id, image_path):
    try:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=channel_id, photo=photo)
    except Exception as e:
        print(f"Не удалось отправить изображение {image_path}: {e}")


def publish_images(directory, interval, channel_id, bot):
    posted_images = set()
    all_images = []
    while True:
        if not all_images:
            all_images = os.listdir(directory)
            all_images = [img for img in all_images if os.path.isfile(os.path.join(directory, img))]
            random.shuffle(all_images)
        for image in all_images:
            if image not in posted_images:
                image_path = os.path.join(directory, image)
                post_photo(bot, channel_id, image_path)
                posted_images.add(image)
                time.sleep(interval)
        if len(posted_images) == len(all_images):
            posted_images.clear()


def main():
    parser = argparse.ArgumentParser(description="Publish photos to a Telegram channel at regular intervals.")
    parser.add_argument(
        '--interval',
        type=int,
        default=14400,
        help="Интервал в секундах между публикацией изображений. По умолчанию 14400 секунд (4 часа)."
    )
    args = parser.parse_args()
    env = Env()
    env.read_env("token.env")
    token = env.str("TG_SPACE_TOKEN")
    channel_id = env.str("TG_CHANEL_NAME")
    image_directory = "images"
    bot = Bot(token=token)
    publish_images(image_directory, args.interval, channel_id, bot)


if __name__ == '__main__':
    main()
