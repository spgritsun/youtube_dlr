import streamlit as st
from pytube import YouTube
import os

# Название заголовка
st.title("Загрузите видео с YouTube")

# Поле для вставки ссылки на видео
video_url = st.text_input("Введите URL видео с YouTube:")

# Кнопка, которая выполняет все действия
if st.button("Скачать видео"):
    if video_url:
        try:
            # Загружаем видео с YouTube
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()

            # Получаем временное имя сохраненного файла
            file_path = stream.download(output_path=".")

            # Передача файла пользователю через Streamlit
            with open(file_path, "rb") as video_file:
                st.download_button(
                    label="Нажмите для скачивания",
                    data=video_file,
                    file_name=f"{yt.title}.mp4",
                    mime="video/mp4"
                )

            # Удаляем локальный файл после загрузки
            os.remove(file_path)
        except Exception as e:
            st.error(f"Ошибка при загрузке видео: {e}")
    else:
        st.warning("Пожалуйста, введите корректный URL видео!")