import yt_dlp
import os

def download_audio(link):
    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
        info_dict = video.extract_info(link, download = True)
        video_title = info_dict['title']
        video.download(link) 
        return video_title + '.mp3'
