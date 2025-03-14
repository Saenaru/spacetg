import requests
import argparse
from handle_image_file import download_image, get_image_extension


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


def get_latest_launch_id():
    latest_launch_url = "https://api.spacexdata.com/v5/launches/latest"
    response = requests.get(latest_launch_url)
    response.raise_for_status()
    latest_launch_data = response.json()
    return latest_launch_data['id']


def main():
    parser = argparse.ArgumentParser(description='Download images from a SpaceX launch.')
    parser.add_argument('--launch_id', type=str, help='SpaceX launch ID to download images from')
    args = parser.parse_args()
    if args.launch_id:
        print(f"Скачивание изображений для запуска с ID: {args.launch_id}")
        fetch_spacex_images(args.launch_id)
    else:
        latest_launch_id = get_latest_launch_id()
        print(f"Скачивание изображений для последнего запуска с ID: {latest_launch_id}")
        fetch_spacex_images(latest_launch_id)


if __name__ == "__main__":
    main()
