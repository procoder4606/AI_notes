import yt_dlp
import os

def download_video(url):
    """
    Download YouTube video as video.mp4 and extract audio as audio.wav.
    Returns (video_path, audio_path)
    """
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': 'video.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Extract audio using ffmpeg
    os.system('ffmpeg -y -i video.mp4 -vn audio.wav')
    return 'video.mp4', 'audio.wav'