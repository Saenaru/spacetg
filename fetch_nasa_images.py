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
    data = response.json()
    for i, item in enumerate(data):
        if item.get('media_type') == 'image' and 'url' in item:
            photo_url = item['url']
            save_path = f'images/nasa_apod_{i}{get_image_extension(photo_url)}'
            try:
                download_image(photo_url, save_path)
                print(f"NASA Фото {i+1} загружено и сохранено как '{save_path}'.")
            except requests.HTTPError as e:
                print(f"Не удалось загрузить NASA фото {i+1}: {e}")
        else:
            print(f"Пропуск файла {i+1}, так как это не изображение.")


def main():
    env = Env()
    env.read_env("token.env")
    api_key = env.str("NASA_API_KEY")
    fetch_nasa_images(api_key)


if __name__ == "__main__":
    main()
