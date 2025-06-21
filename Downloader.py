import os
import yt_dlp

#pip install yt-dlp
#pip install ffmpeg-python
#pip install ffmpeg
def get_video_url():
    """Запрашивает ссылку на YouTube-видео у пользователя и проверяет её."""
    url = input("📥 Вставьте ссылку на YouTube-видео:\n").strip()
    if not url.startswith("http"):
        print("❗ Неверная ссылка.")
        return None
    return url

def get_format_choice():
    """Запрашивает у пользователя выбор формата для скачивания."""
    choice = input("📼 Выберите формат: [1] mp4 (видео) | [2] mp3 (аудио): ").strip()
    if choice in ['1', '2']:
        return choice
    print("❗ Неверный выбор формата.")
    return None

def create_save_directory(format_choice):
    """Создает директорию для сохранения скачанных файлов на рабочем столе."""
    user_profile = os.environ.get('USERPROFILE') or os.path.expanduser('~')
    folder_name = 'Downloaded_videos' if format_choice == '1' else 'Downloaded_audios'
    save_dir = os.path.join(user_profile, 'OneDrive', 'Рабочий стол', folder_name)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def setup_ffmpeg():
    """Возвращает путь к исполняемому файлу ffmpeg."""
    ffmpeg_exe = r'C:\Users\User\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe'
    if not os.path.isfile(ffmpeg_exe):
        print(f"❗ Не удается найти ffmpeg по пути: {ffmpeg_exe}. Пожалуйста, установите ffmpeg.")
        return None
    return ffmpeg_exe

def configure_download_options(format_choice, save_dir):
    """Настраивает опции загрузки для yt-dlp."""
    ydl_opts = {
        'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ffmpeg_location': setup_ffmpeg(),
        'nocheckcertificate': True
    }
    if format_choice == '1':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'
    elif format_choice == '2':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        })
    return ydl_opts

def download_video(url, ydl_opts):
    """Скачивает видео с использованием yt-dlp."""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Скачивание завершено!")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

def main():
    url = get_video_url()
    if url is None:
        return

    format_choice = get_format_choice()
    if format_choice is None:
        return

    save_dir = create_save_directory(format_choice)
    ydl_opts = configure_download_options(format_choice, save_dir)
    download_video(url, ydl_opts)

# 🚀 Старт
if __name__ == "__main__":
    main()