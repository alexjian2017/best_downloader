import requests
import m3u8
import re
import os
import json
import time
from Crypto.Cipher import AES
# pip install pycryptodome

from encode import ffmpegEncode
from crawler import Scrape, Chrome_webdriver
import constant

# 教學影片
# https://www.youtube.com/watch?v=bytnxnZFLeg


def simple_download(url: str, filename: str, chunk_size: int = 1024, target_folder: str = 'result') -> None:
    """
    You already have url link with video in it
    """
    os.chdir(target_folder)
    start_time = time.time()
    r = requests.get(url, stream=True)
    with open(f'{filename}.mp4', 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
    end_time = time.time()
    print(f'花費 {((end_time - start_time) / 60):.2f} 分鐘 下載完成 !')


def m3u8_download(url: str, filename: str, high_quality: int) -> None:
    if not filename:
        url_split = url.split('/')
        filename = url_split[-1] if url_split[-1] else url_split[-2]

    # use selenium to grab m3u8 url
    dr = Chrome_webdriver()
    dr.get(url)
    result = re.search("https://.+m3u8", dr.page_source)
    if result:
        m3u8url = result[0]
    else:
        m3u8url = input("這網址找不到符合的m3u8 url，請你提供給我: ").strip()
    baseurl = '/'.join(m3u8url.split('/')[:-1])
    print(f'm3u8url: {m3u8url}')
    print(f'baseurl: {baseurl}')
    try:
        # m3u8.load/loads 區別是 load 接 url, loads 接 text
        # r = requests.get(m3u8url)
        # m3u8_master = m3u8.loads(r.text, headers=constant.Fake_Browser_Headers)
        m3u8_master = m3u8.load(m3u8url, headers=constant.Fake_Browser_Headers)
        # with open('aa.txt', 'w') as f:
        #     f.write(json.dumps(m3u8_master.data))
    except Exception as e:
        print(f'{e}/n你提供的url，並無法造訪，麻煩確認之後，再進行嘗試')
        return

    # if there are multiple resolutions
    if m3u8_master.playlists:
        print('!! There are multiple resolutions!!')
        #  usually, 0 for lowest quality, -1 for highest
        if high_quality:
            playlist_url = m3u8_master.playlists[-1].uri
        else:
            playlist_url = m3u8_master.playlists[0].uri
        if not playlist_url.startswith('http'):
            playlist_url = baseurl + '/' + playlist_url
        print(f'playlist_url: {playlist_url}')
        m3u8_master = m3u8.load(
            playlist_url, headers=constant.Fake_Browser_Headers)

    # if m3u8 is encoded
    m3u8uri, m3u8iv, ci = '', '', ''
    for key in m3u8_master.keys:
        if key:
            m3u8uri = key.uri
            m3u8iv = key.iv
    if m3u8uri:
        if not m3u8uri.startswith('http'):
            m3u8uri = baseurl + '/' + m3u8uri

        response = requests.get(
            m3u8uri, headers=constant.Fake_Browser_Headers, timeout=10)
        contentKey = response.content

        vt = m3u8iv.replace("0x", "")[:16].encode()  # IV取前16位
        ci = AES.new(contentKey, AES.MODE_CBC, vt)  # 建構解碼器
    # print(f'm3u8uri: {m3u8uri}')
    # print(f'm3u8iv: {m3u8iv}')
    # print(f'ci: {ci}')

    # store .ts file in ts_list
    ts_list = []
    for segment in m3u8_master.segments:
        segment_url = segment.uri
        if not segment_url.startswith('http'):
            segment_url = baseurl + '/' + segment_url
        ts_list.append(segment_url)

    # crawl .ts file from internet(using request)
    crawler = Scrape(filename, ci, ts_list)
    # crawler = Scrape(filename, ci, ts_list[:10])
    crawler.startCrawl()

    # transfer to a better video form
    ffmpegEncode('result', filename, 2)


if __name__ == '__main__':
    url = input('請輸入你要下載的影片網址: ').strip()
    filename = input('請輸入你要命名的檔名: ').strip()
    high_quality = input('是否下載最高畫質(Y/N)? ').strip().lower()
    high_quality = 1 if high_quality == 'y' else 0
    # simple_download(url, filename)
    m3u8_download(url, filename, high_quality)
