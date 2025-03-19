import requests
from environs import Env
from datetime import datetime, timedelta
from handle_image_file import download_image, get_image_extension


def fetch_nasa_images(api_key):
    end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=35)).strftime('%Y-%m-%d')
    api_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    apod_images = response.json()
    for image_index, image_metadata in enumerate(apod_images, start=1):
        if image_metadata.get('media_type') != 'image' or 'url' not in image_metadata:
            print(f"Пропуск файла {image_index}, так как это не изображение.")
            continue
        image_url = image_metadata['url']
        image_extension = get_image_extension(image_url)
        save_path = f'images/nasa_apod_{image_index}{image_extension}'
        try:
            download_image(image_url, save_path)
            print(f"NASA Фото {image_index} загружено и сохранено как '{save_path}'.")
        except requests.HTTPError as e:
            print(f"Не удалось загрузить NASA фото {image_index}: {e}")


def main():
    env = Env()
    env.read_env("token.env")
    api_key = env.str("NASA_API_KEY")
    fetch_nasa_images(api_key)


if __name__ == "__main__":
    main()
