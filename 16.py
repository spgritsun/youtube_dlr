import PySimpleGUI as sg
import yt_dlp
import os
import re


# Функция для обновления индикатора выполнения
def update_progress_bar(window, progress_info):
    total_bytes = progress_info.get("total_bytes") or progress_info.get("total_bytes_estimate", 1)
    downloaded_bytes = progress_info.get("downloaded_bytes", 0)
    progress_percent = int(downloaded_bytes / total_bytes * 100)
    window["-PROGRESS_BAR-"].update(progress_percent)


# Основной интерфейс
sg.theme("LightBlue3")
layout = [
    [sg.Text("Введите ссылку на видео YouTube:")],
    [sg.Input(key="-URL-", size=(40, 1))],
    [sg.Text("Выберите папку для сохранения:")],
    [sg.Input(key="-FOLDER-", size=(30, 1)), sg.FolderBrowse("Обзор")],
    [sg.ProgressBar(max_value=100, orientation="h", size=(40, 20), key="-PROGRESS_BAR-")],
    [sg.Button("Скачать"), sg.Button("Выход")],
]

window = sg.Window("YouTube Downloader", layout)

youtube_url_pattern = r"^https?://(www\.)?(youtube\.com|youtu\.be)/.+"

# Обработка событий GUI
while True:
    event, values = window.read(timeout=100)  # Периодическое обновление интерфейса
    if event == sg.WINDOW_CLOSED or event == "Выход":
        break
    if event == "Скачать":
        video_url = values["-URL-"]
        save_path = values["-FOLDER-"]

        if not video_url:
            sg.popup_error("Введите ссылку на видео.")
            continue

        if not re.match(youtube_url_pattern, video_url):
            sg.popup_error("Введите корректную ссылку на видео.")
            continue

        if not save_path:
            sg.popup_error("Выберите папку для сохранения видео.")
            continue

        # Перед началом загрузки сбрасываем progress bar
        window["-PROGRESS_BAR-"].update(0)

        # Настройка параметров для yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [
                {'key': 'FFmpegVideoConvertor', 'preferredcodec': 'mp4'}
            ],
            'progress_hooks': [lambda d: update_progress_bar(window, d)],  # Хук для обновления прогресса
        }

        # Загрузка видео
        try:
            sg.popup("Начинаем загрузку. Это может занять некоторое время...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            sg.popup("Видео успешно скачано!", title="Успех")
        except yt_dlp.utils.DownloadError as e:
            sg.popup_error(f"Ошибка загрузки: {e}")
        except Exception as e:
            sg.popup_error(f"Произошла ошибка: {e}")

# Закрыть окно после завершения
window.close()
