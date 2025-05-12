import streamlit as st
import yt_dlp
import os
import tempfile
from pathlib import Path


def update_progress(progress_hook, progress_bar, status_text):
    if progress_hook['status'] == 'downloading':
        percent = progress_hook['downloaded_bytes'] / progress_hook['total_bytes']
        progress_bar.progress(min(percent, 1.0))
        status_text.text(f"Прогресс: {percent:.1%}")


def main():
    st.title("📥 YouTube Downloader")

    url = st.text_input("Вставьте ссылку на YouTube видео:")

    if st.button("Скачать"):
        if not url.strip():
            st.error("Введите URL видео")
            return

        progress_bar = st.progress(0)
        status_text = st.empty()

        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                'format': 'bestvideo[height<=1080]+bestaudio/best',
                'progress_hooks': [lambda d: update_progress(d, progress_bar, status_text)],
                'quiet': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                    # Читаем файл в память
                    with open(filename, 'rb') as f:
                        video_bytes = f.read()

                    # Генерируем имя файла
                    safe_title = "".join(c for c in info['title'] if c.isalnum() or c in (' ', '-'))
                    download_name = f"{safe_title}.mp4"

                    # Очищаем прогресс-бар
                    progress_bar.empty()
                    status_text.empty()

                    # Показываем информацию о видео
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(info.get('thumbnail'), width=300)
                    with col2:
                        st.subheader(info['title'])
                        st.caption(f"Длительность: {info['duration'] // 60}:{info['duration'] % 60:02d}")

                    # Предлагаем скачивание
                    st.success("✅ Видео успешно загружено на наш сервер!")
                    st.download_button(
                        label="🔽 Скачать видео на компьютер",
                        data=video_bytes,
                        file_name=download_name,
                        mime="video/mp4",
                        key="download_btn"
                    )

                    st.balloons()

            except Exception as e:
                status_text.error(f"Ошибка: {str(e)}")
                progress_bar.empty()


if __name__ == "__main__":
    main()