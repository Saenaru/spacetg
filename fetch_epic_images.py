import requests
from environs import Env
from datetime import datetime
from handle_image_file import download_image


def download_epic_images(api_key, limit=10):
    base_api_url = "https://api.nasa.gov/EPIC/api/natural"
    response = requests.get(base_api_url, params={'api_key': api_key})
    response.raise_for_status()
    epic_images = response.json()
    count = 0
    for epic_image in epic_images:
        if count >= limit:
            break
        identifier = epic_image['identifier']
        date_str = epic_image['date']
        date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        date_path = date_time.strftime('%Y/%m/%d')
        image_base_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_path}/png/epic_1b_{identifier}.png"
        image_url = requests.Request('GET', image_base_url, params={'api_key': api_key}).prepare().url
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
    api_key = env.str("NASA_API_KEY")
    download_epic_images(api_key)


if __name__ == "__main__":
    main()
