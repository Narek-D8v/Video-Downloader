import os
import yt_dlp

#pip install yt-dlp
#pip install ffmpeg-python
#pip install ffmpeg
def get_video_url():
    """Requests a YouTube video link from the user and verifies it."""
    url = input("📥 Paste the link to the YouTube video:\n").strip()
    if not url.startswith("http"):
        print("❗ Invalid link.")
        return None
    return url

def get_format_choice():
    """Prompts the user to select a download format."""
    choice = input("📼 Select format: [1] mp4 (video) | [2] mp3 (audio): ").strip()
    if choice in ['1', '2']:
        return choice
    print("❗Incorrect format selection.")
    return None

def create_save_directory(format_choice):
    """Creates a directory for saving downloaded files on the desktop."""
    user_profile = os.environ.get('USERPROFILE') or os.path.expanduser('~')
    folder_name = 'Downloaded_videos' if format_choice == '1' else 'Downloaded_audios'
    save_dir = os.path.join(user_profile, 'OneDrive', 'Рабочий стол', folder_name)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def setup_ffmpeg():
    """Returns the path to the ffmpeg executable."""
    ffmpeg_exe = r'C:\Users\User\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe'
    if not os.path.isfile(ffmpeg_exe):
        print(f"❗ Unable to find ffmpeg in path: {ffmpeg_exe}. Please install ffmpeg.")
        return None
    return ffmpeg_exe

def configure_download_options(format_choice, save_dir):
    """Configures boot options for yt-dlp."""
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
    """Downloads video using yt-dlp."""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

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

# 🚀 Start
if __name__ == "__main__":
    main()
