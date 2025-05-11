import streamlit as st
import yt_dlp
from pathlib import Path
import os

# Обновление прогресс-бара
def update_progress_bar(progress, bar):
    if 'total_bytes' in progress and 'downloaded_bytes' in progress:
        total = progress['total_bytes']
        downloaded = progress['downloaded_bytes']
        percent = int(downloaded / total * 100)
        bar.progress(percent / 100)  # Обновляем Streamlit прогресс-бар

# Проверка, установлен ли FFmpeg
def is_ffmpeg_installed():
    if os.system("ffmpeg -version") != 0:
        st.warning("FFmpeg не установлен. Убедитесь, что он установлен для работы приложения.")

# Streamlit интерфейс
def main():
    st.title("Сохранение видео с YouTube (с использованием yt-dlp)")

    # Проверяем наличие FFmpeg
    is_ffmpeg_installed()

    # Поле для ввода ссылки на видео
    video_url = st.text_input("Введите ссылку на YouTube", placeholder="Например, https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # Поле для ввода пути загрузки (вместо выбора через проводник указываем текстовый путь)
    save_path = st.text_input("Укажите папку для сохранения видео (полный путь)", placeholder="Укажите полный путь к папке")

    # Кнопка "Скачать"
    if st.button("Скачать видео"):

        # Проверяем введенные данные
        if not video_url.strip() or not save_path.strip():
            st.error("Введите ссылку на видео и укажите путь загрузки.")
            return

        # Проверяем, существует ли путь
        save_dir = Path(save_path)
        if not save_dir.exists():
            st.error(f"Указанный путь не существует: {save_path}")
            return

        # Прогресс-бар
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Настройки yt-dlp
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Указывает путь сохранения
            'format': 'bestvideo[height<=1080]+bestaudio/best',  # Загрузка видео в 1080p с аудио
            'merge_output_format': 'mp4',  # Сохранение в MP4
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'  # Если требуется перекодирование
            }],
            'progress_hooks': [lambda d: update_progress_bar(d, progress_bar)]  # Обновляем прогресс-бар Streamlit
        }

        # Начинаем загрузку
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                st.info("Начинается загрузка...")
                ydl.download([video_url])
                st.success(f"Видео успешно скачано в папку: {save_path}")
        except Exception as e:
            st.error(f"Произошла ошибка во время скачивания: {e}")


# Запускаем Streamlit приложение
if __name__ == "__main__":
    main()