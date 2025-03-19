import requests
import argparse
from handle_image_file import download_image, get_image_extension


def download_spacex_launch_images(launch_id):
    launch_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(launch_url)
    response.raise_for_status()
    spacex_launch_data = response.json()
    photos = spacex_launch_data.get("links", {}).get("flickr", {}).get("original", [])
    for image_index, photo_url in enumerate(photos, start=1):
        save_path = f'images/spacex_{image_index}{get_image_extension(photo_url)}'
        try:
            download_image(photo_url, save_path)
            print(f"Фото {image_index} загружено и сохранено как '{save_path}'.")
        except requests.HTTPError as e:
            print(f"Не удалось загрузить фото {image_index}: {e}")


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
        download_spacex_launch_images(args.launch_id)
    else:
        latest_launch_id = get_latest_launch_id()
        print(f"Скачивание изображений для последнего запуска с ID: {latest_launch_id}")
        download_spacex_launch_images(latest_launch_id)


if __name__ == "__main__":
    main()
