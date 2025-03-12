import os
import requests
import urllib.parse
from datetime import datetime, timedelta
from environs import Env


def download_image(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_images(launch_id):
    launch_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(launch_url)
    response.raise_for_status()
    launch_data = response.json()
    photos = launch_data.get("links", {}).get("flickr", {}).get("original", [])
    for i, photo_url in enumerate(photos):
        save_path = f'images/spacex_{i}{get_image_extension(photo_url)}'
        try:
            download_image(photo_url, save_path)
            print(f"Фото {i+1} загружено и сохранено как '{save_path}'.")
        except requests.HTTPError as e:
            print(f"Не удалось загрузить фото {i+1}: {e}")



def get_image_extension(url):
    parsed_url = urllib.parse.urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    extension = os.path.splitext(file_name)[-1]
    return extension


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
    image_urls = [item['url'] for item in data if 'url' in item]
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


def download_epic_images(api_key, limit=10):
    api_url = f"https://api.nasa.gov/EPIC/api/natural?api_key={api_key}"
    response = requests.get(api_url)
    response.raise_for_status()
    epic_data = response.json()
    count = 0
    for item in epic_data:
        if count >= limit:
            break
        identifier = item['identifier']
        date_str = item['date']
        date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        date_path = date_time.strftime('%Y/%m/%d')
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_path}/png/epic_1b_{identifier}.png?api_key={api_key}"
        save_path = f"images/epic_{identifier}.png"
        try:
            download_image(image_url, save_path)
            print(f"Downloaded {save_path}")
            count += 1
        except requests.HTTPError as e:
            print(f"Failed to download {identifier}: {e}")


def main():
    env = Env()
    env.read_env("token.env")
    launch_id = "61eefaa89eb1064137a1bd73"
    fetch_spacex_images(launch_id)
    api_key = env.str("NASA_API_KEY")
    fetch_nasa_images(api_key)
    download_epic_images(api_key)


if __name__ == "__main__":
    main()
