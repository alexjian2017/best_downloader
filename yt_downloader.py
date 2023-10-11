from pytube import YouTube
from yt_dlp import YoutubeDL
import os


def download_videos_by_dlp(url: str, target_folder: str = 'result') -> None:
    os.chdir(target_folder)
    try:
        with YoutubeDL() as ydl:
            ydl.download(url)
    except Exception as e:
        print(e)


def download_audio_by_pytube(url: str, target_folder: str = 'result') -> None:
    try:
        # yt = YouTube(url, use_oauth=True,
        #              allow_oauth_cache=True)
        yt = YouTube(url)
        title = yt.title
        print("Title: ", title)
        print("Views: ", yt.views)
        file = yt.streams.filter(only_audio=True).first()
        file.download(target_folder, f'{title}.mp3')
    except Exception as e:
        print(e)
    else:
        print(f"' {yt.title} '已經下載完成")


def download_videos_by_pytube(url: str, high_quality: int, target_folder: str = 'result') -> None:
    try:
        yt = YouTube(url)
        print("Title: ", yt.title)
        print("Views: ", yt.views)
        if high_quality:
            file = yt.streams.get_highest_resolution()
        else:
            file = yt.streams.get_lowest_resolution()
        file.download(target_folder)
    except Exception as e:
        print(e)
    else:
        print(f"' {yt.title} '已經下載完成")


def yt_download(url: str, high_quality: int):
    while 1:
        mp3_or_not = input("是否僅下載聲音檔(Y/N/ex): ").strip().lower()
        if mp3_or_not == 'ex':
            download_videos_by_dlp(url)
        elif mp3_or_not == 'y':
            download_audio_by_pytube(url)
        elif mp3_or_not == 'n':
            download_videos_by_pytube(url, high_quality)
        else:
            print("輸入不符合要求，請重新輸入")
            continue
        break


if __name__ == '__main__':
    url = input('請輸入你要下載的影片網址: ').strip()
    high_quality = input('是否下載最高畫質(Y/N)? ').strip().lower()
    high_quality = 1 if high_quality == 'y' else 0
    yt_download(url, high_quality)
