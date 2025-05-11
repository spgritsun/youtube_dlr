import os
import yt_dlp
import streamlit as st
from pathlib import Path


# Определение папки "Загрузки" для операционной системы
def get_download_folder():
    if os.name == "nt":  # Windows
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    else:  # macOS/Linux
        return os.path.join(os.path.expanduser("~"), "Downloads")


# Обновление прогресс-бара
def update_progress_bar(d, progress_bar):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total:
            progress_bar.progress(min(downloaded / total, 1.0))


# Приложение Streamlit
def main():
    st.title("Скачиватель видео с YouTube")

    # Поле для ввода ссылки
    video_url = st.text_input("Введите URL-адрес YouTube видео:", "")

    # Кнопка для запуска скачивания
    if st.button("Скачать видео"):
        if not video_url:
            st.error("Пожалуйста, введите URL видео!")
            return

        # Путь к папке загрузок
        save_path = Path(get_download_folder())

        # Прогресс-бар и статус
        progress_bar = st.progress(0)

        # Настройки yt-dlp
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'progress_hooks': [lambda d: update_progress_bar(d, progress_bar)]
        }

        # Загрузка видео
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                st.info("Начинается загрузка...")
                ydl.download([video_url])
                st.success(f"Видео успешно скачано в папку: {save_path}")
        except Exception as e:
            st.error(f"Произошла ошибка во время скачивания: {e}")


if __name__ == "__main__":
    main()