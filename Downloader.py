import os
import yt_dlp

VIDEO_DIR = r"C:\Users\User\OneDrive\Рабочий стол\Downloaded_videos"
AUDIO_DIR = r"C:\Users\User\OneDrive\Рабочий стол\Downloaded_audios"
FFMPEG_DIR = r"C:\Users\User\ffmpeg\ffmpeg-7.1.1-essentials_build\bin"
FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')


def check_ffmpeg():
    if not os.path.isfile(FFMPEG_EXE):
        print(f"\n❌ FFmpeg не найден по пути: {FFMPEG_EXE}")
        exit(1)


def get_video_url():
    url = input("📥 Вставьте ссылку на YouTube-видео:\n> ").strip()
    if not url.startswith("http"):
        print("❗ Неверная ссылка.")
        return None
    return url


def get_format_choice():
    print("\n📼 Выберите формат:")
    print("[1] Видео (.mp4 с AAC)")
    print("[2] Аудио (.mp3)")
    choice = input("> ").strip()
    if choice in ['1', '2']:
        return choice
    print("❗ Неверный выбор.")
    return None


def build_yt_dlp_options(format_choice):
    if format_choice == '1':
        save_dir = VIDEO_DIR
        opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'nocheckcertificate': True,
            'ffmpeg_location': FFMPEG_DIR,
            'merge_output_format': 'mp4',
            'postprocessor_args': [
                '-c:v', 'copy',      # видео — копируем
                '-c:a', 'aac',       # перекодируем аудио в AAC
                '-b:a', '192k'       # качество
            ],
            'cachedir': False,
        }
    else:
        save_dir = AUDIO_DIR
        opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'nocheckcertificate': True,
            'ffmpeg_location': FFMPEG_DIR,
            'cachedir': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    os.makedirs(save_dir, exist_ok=True)
    return opts, save_dir


def download_content(url, options):
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"\n❗ Ошибка при скачивании: {e}")
        return False


def main():
    print("🎬 YouTube Downloader")
    print("=" * 30)
    check_ffmpeg()

    while True:
        url = get_video_url()
        if not url:
            continue

        fmt = get_format_choice()
        if not fmt:
            continue

        ydl_opts, output_dir = build_yt_dlp_options(fmt)
        print("\n⏳ Начинаю скачивание...")
        success = download_content(url, ydl_opts)

        if success:
            print(f"✅ Файл успешно скачан в: {output_dir}")
        else:
            print("⚠️ Ошибка при скачивании.")

        again = input("\n🔄 Скачать ещё? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("\n👋 Завершено.")


if __name__ == "__main__":
    main()
