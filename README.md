# Документация по коду `Космический Телеграм` / Code documentation `Space Telegram`

## Оглавление / Table of Contents

- [Русский](#русский)
- [English](#english)

---

## Русский

## Описание программы:
Программа подключается к NASA и SPACEX API и позволяет скачать фотографии космоса. А также публикует фотографии из директории в Telegram-канал.

## Как установить

1. Python3 должен быть уже установлен.
2. Создайте виртуальное окружение venv для изоляции зависимостей.

```bash
python -m venv .venv
```

Активация виртуального окружения:
- На Windows:
```bash
.venv\Scripts\activate
```
- На MacOS и Linux:
```bash
source .venv/bin/activate
```

Выполните команду:
```bash
pip install -r requirements.txt
   ```

3. Это приложение использует файл .env для хранения конфиденциальных и конфигурируемых параметров настройки.

В корневом каталоге проекта создайте файл «token.env», каждая переменная среды указывается с новой строки в формате КЛЮЧ=значение. Пример:

```plaintext
NASA_API_KEY=***
TG_SPACE_TOKEN=***
```

Храните `.env` в безопасности: Убедитесь, что файл .env не попадает в систему контроля версий, как например Git, добавив его в .gitignore.

## Скрипт `fetch_spacex_images.py`:
Скрипт скачивает фотографии с последнего запуска [SpaceX REST API](https://github.com/r-spacex/SpaceX-API). Если в последнем запуске не было фотографий, то для скачивания фото нужно указать launch_id, на котором были запуски, например:`61eefaa89eb1064137a1bd73`
Пример:
```
python fetch_spacex_images.py
Скачивание изображений для последнего запуска с ID: 62dd70d5202306255024d139
```

```
python fetch_spacex_images.py --launch 61eefaa89eb1064137a1bd73
Фото 1 загружено и сохранено как 'images/spacex_0.jpg'.
Фото 2 загружено и сохранено как 'images/spacex_1.jpg'.
...
```

## Скрипт `fetch_nasa_images.py`:
Скрипт скачивает красивые фотографии снимков космоса от [NASA APOD API](https://api.nasa.gov/#apod) за последние 35 дней. В файлах попадаются так же и видео, скрипт их пропускает. Для работы скрипта нужно зарегистрироваться и получить API Key.
Пример:

```
python fetch_nasa_images.py                                       
NASA Фото 1 загружено и сохранено как 'images/nasa_apod_0.jpg'.
NASA Фото 2 загружено и сохранено как 'images/nasa_apod_1.jpg'.
NASA Фото 3 загружено и сохранено как 'images/nasa_apod_2.jpg'.
NASA Фото 4 загружено и сохранено как 'images/nasa_apod_3.jpg'.
Пропуск файла 5, так как это не изображение.
NASA Фото 6 загружено и сохранено как 'images/nasa_apod_5.jpg'.
...
```

## Скрипт `fetch_epic_images.py`:
Скрипт скачивает `эпичные` фотографии земли [NASA EPIC API](https://api.nasa.gov/#epic). Для работы скрипта нужно зарегистрироваться и получить API Key.

Пример:
```
python fetch_epic_images.py
Downloaded images/epic_20250312001752.png
Downloaded images/epic_20250312020554.png
...
```

## Скрипт `photo_of_space_bot.py`:
Скрипт добавляет фото с дериктории images в телеграмм канал от лица бота. Для отправки случайного фото нужно написать боту `/post`. Для отправки нужного фото нужно прописать название фотографии: `/post epic_20250310024318.png`
Запуск скрипта:

```
python photo_of_space_bot.py
```

## Скрипт `photo_of_space_infinite_bot.py`:
Скрипт добавляет фото с директории images в телеграм канал от лица бота с интервалом 4 часа(14400 секунд). Если нужен другой интервал, то можно указать его в аргументах при запуске скрипта.
Пример:

```
python photo_of_space_infinite_bot.py --interval 10
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).


---

## English

## Program description:
The program connects to the NASA and SPACEX API and allows you to download photos of space. He also publishes photos from the directory to the Telegram channel.

## How to install

1. Python3 must already be installed.
2. Create a venv virtual environment to isolate dependencies

```bash
python -m venv .venv
```

Activating the virtual environment:
- On Windows:
```bash
.venv\Scripts\activate
```
- On macOS and Linux:
```bash
source .venv/bin/activate
```

Run the command:
```bash
pip install -r requirements.txt
```

3. This application uses a file.env for storing confidential and configurable settings.

In the root directory of the project, create the "token.env" file. Each environment variable is specified from a new line in the KEY=value format. Example:

```plaintext
NASA_API_KEY=***
TG_SPACE_TOKEN=***
```

Keep `.env` safe: Make sure that the file .env is not included in the version control system, such as Git, by adding it to .gitignore.

## Script `fetch_spacex_images.py`:
The script downloads photos from the last launch [SpaceX REST API](https://github.com/r-spacex/SpaceX-API). If there were no photos at the last launch, then to download the photo, you need to specify the launch_id on which the launches were, for example:`61eefaa89eb1064137a1bd73`
Example:
```
python fetch_spacex_images.py
Downloading images for the latest launch with ID: 62dd70d5202306255024d139
```

```
python fetch_spacex_images.py --launch 61eefaa89eb1064137a1bd73
Фото 1 загружено и сохранено как 'images/spacex_0.jpg'.
Фото 2 загружено и сохранено как 'images/spacex_1.jpg'.
...
```

## Script `fetch_nasa_images.py`:
The script downloads beautiful photos of space images from [NASA APOD API](https://api.nasa.gov/#apod) for the last 35 days. There are also videos in the files, the script skips them. To run the script, you need to register and get an API Key.
Example:

```
python fetch_nasa_images.py                                       
NASA Фото 1 загружено и сохранено как 'images/nasa_apod_0.jpg'.
NASA Фото 2 загружено и сохранено как 'images/nasa_apod_1.jpg'.
NASA Фото 3 загружено и сохранено как 'images/nasa_apod_2.jpg'.
NASA Фото 4 загружено и сохранено как 'images/nasa_apod_3.jpg'.
Пропуск файла 5, так как это не изображение.
NASA Фото 6 загружено и сохранено как 'images/nasa_apod_5.jpg'.
...
```

## Script `fetch_epic_images.py`:
Script downloads `epic` photos of earth [NASA EPIC API](https://api.nasa.gov/#epic). To run the script, you need to register and get an API Key.

Example:
```
python fetch_epic_images.py
Downloaded images/epic_20250312001752.png
Downloaded images/epic_20250312020554.png
...
```

## Script `photo_of_space_bot.py`:
The script adds a photo from the images directory to the telegram channel on behalf of the bot. To send a random photo, you need to write to the bot `/post`. To send the desired photo, you need to specify the name of the photo: `/post epic_20250310024318.png`
Running the script:

```
python photo_of_space_bot.py
```

## Script `photo_of_space_infinite_bot.py`:
The script adds a photo from the images directory to the telegram channel on behalf of the bot with an interval of 4 hours (14400 seconds). If you need a different interval, you can specify it in the arguments when running the script.
Example:

```
python photo_of_space_infinite_bot.py --interval 10
```

## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).