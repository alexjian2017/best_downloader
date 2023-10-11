from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
import os
import shutil
import random
from concurrent.futures import ThreadPoolExecutor

import constant


class Chrome_webdriver(webdriver.Chrome):
    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('log-level=3')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument(
            f"user-agent={constant.Fake_User_Agent[0]}")
        super(Chrome_webdriver, self).__init__(
            options=options)


class Scrape():
    """
    ci is Crypto.Cipher._mode_cbc.CbcMode object after AES
    """

    def __init__(self, filename: str, ci, ts_list: list[str], target_folder: str = 'result', temp_folder: str = 'temp123'):
        self.filename = filename
        self.ci = ci
        self.ts_list = ts_list
        self.target_folder = target_folder
        self.temp_folder = temp_folder

    def single_scrape(self, url: str, times: int = 1) -> None:
        if times > 5:
            return
        response = requests.get(
            url, headers={"User-Agent": random.choice(constant.Fake_User_Agent)})
        if response.status_code == 200:
            content_ts = response.content
            if self.ci:
                content_ts = self.ci.decrypt(content_ts)  # 解碼
            with open(os.path.join(self.temp_folder, url.split('/')[-1]), 'wb') as f:
                f.write(content_ts)
        else:
            print(f'第{times}次失敗: {url}')
            self.single_scrape(self, url, times+1)

    def startCrawl(self) -> None:
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
        os.mkdir(self.temp_folder)

        start_time = time.time()
        print(f'開始下載 {len(self.ts_list)} 個檔案..', end='')
        print(f'預計等待時間: {len(self.ts_list) / 150:.2f} 分鐘 (視影片長度與網路速度而定)')
        with ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(self.single_scrape, self.ts_list)
        end_time = time.time()
        print(f'花費 {((end_time - start_time) / 60):.2f} 分鐘 爬取完成 !')

        self.mergeCrawl()
        shutil.rmtree(self.temp_folder)

    def mergeCrawl(self) -> None:
        if not os.path.exists(self.target_folder):
            os.mkdir(self.target_folder)

        start_time = time.time()
        with open(os.path.join(self.target_folder, f"{self.filename}.ts"), 'wb') as f1:
            for url in self.ts_list:
                file = url.split('/')[-1]
                try:
                    with open(os.path.join(self.temp_folder, file), 'rb') as f2:
                        f1.write(f2.read())
                except FileNotFoundError:
                    print(f'{file} 下載失敗，造成影片缺失，請見諒。')
        end_time = time.time()
        print(f'花費 {((end_time - start_time) / 60):.2f} 分鐘 合成完成 !')
