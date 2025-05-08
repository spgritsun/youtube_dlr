import FreeSimpleGUI as sg
import yt_dlp
import functions

functions.is_ffmpeg_installed()

video_source_label = sg.Text('Что скачать с Youtube?')
video_url_box = sg.InputText(tooltip='Введи ссылку на видео', key='video_url')
dist_video_label = sg.Text('Куда скачать?')
dict_folder_box = sg.InputText(tooltip='Выбери папку для сохранения', key='dist_folder')
choose_button = sg.FolderBrowse('Выбрать папку', key='choose_button')
download_button = sg.Button('Скачать', key='download')
exit_button = sg.Button('Выход', key='exit')
window = sg.Window('Загрузчик с Youtube', layout=[[video_source_label, video_url_box],
                                                  [dist_video_label, dict_folder_box, choose_button],
                                                  [download_button, exit_button]])
while True:
    event, values = window.read()
    if event == 'exit' or event == sg.WINDOW_CLOSED:
        break
    if values['video_url']:
        video_url = values['video_url']
    else:
        sg.popup('Введите ссылку на скачивание')
        continue
    if values['choose_button']:
        save_path = values['choose_button']
    else:
        sg.popup('Выберите папку для сохранения видео')
        continue
    match event:
        case 'download':
            ydl_opts = {
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Указываем полный путь к папке
                'format': 'bestvideo[height<=1080]+bestaudio/best',  # Скачиваем видео 1080p с аудио
                'merge_output_format': 'mp4',  # Объединение в формат mp4
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'  # Преобразование в MP4, если требуется
                }]
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                sg.popup(f"Видео успешно скачано и сохранено в папке: {save_path}")

            except Exception as e:
                sg.popup(f"Произошла ошибка во время загрузки: {e}")
                break
window.close()
