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
        video_filename = None
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'cookies': 'cookies.json',  # укажите ваш путь к файлу куки
            'progress_hooks': [lambda d: update_progress_bar(d, progress_bar)]
        }

        # Загрузка видео
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                st.info("Начинается загрузка...")
                info_dict = ydl.extract_info(video_url, download=True)
                video_filename = ydl.prepare_filename(info_dict)
                st.success(f"Видео успешно скачано: {video_filename}")
        except Exception as e:
            st.error(f"Произошла ошибка во время скачивания: {e}")
            return

        # Предоставить кнопку для загрузки видео
        if video_filename:
            # Прочитать файл как бинарные данные
            with open(video_filename, "rb") as file:
                video_data = file.read()
                # Кнопка для загрузки файла
                st.download_button(
                    label="Скачать видео",
                    data=video_data,
                    file_name=os.path.basename(video_filename),
                    mime="video/mp4"
                )


if __name__ == "__main__":
    main()