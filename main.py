from downloader import simple_download, m3u8_download
from yt_downloader import yt_download

TYPE_OF_FUNCTION = 3

if __name__ == '__main__':
    print("歡迎使用下載系統，以下提供3種服務:")
    print("1. Youtube 影片下載功能")
    print("2. 基本影片下載功能")
    print("3. m3u8 影片下載功能")
    while 1:
        choice = input("請依據需求輸入你要使用的功能: ").strip()
        if not choice.isdigit():
            print("輸入不符合要求，請輸入符合要求的數字")
            continue
        choice = int(choice)
        if 0 < choice <= TYPE_OF_FUNCTION:
            break
        else:
            print("輸入不符合要求，請輸入符合要求的數字")

    url = input('請輸入你要下載的影片網址: ').strip()
    filename = input('請輸入你要命名的檔名: ').strip()
    high_quality = input('是否下載最高畫質(Y/N)? ').strip().lower()
    high_quality = 1 if high_quality == 'y' else 0
    if choice == 1:
        yt_download(url, high_quality)
    elif choice == 2:
        simple_download(url, filename)
    else:
        m3u8_download(url, filename, high_quality)
