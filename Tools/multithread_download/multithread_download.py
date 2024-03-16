# -*- coding: utf-8 -*-
# @Time : 2024/3/13 19:02
# @Author : Cola.Lee
# @File : multithread_download.py
# @desc :
import requests

from tqdm import tqdm
from pathlib import Path
from threading import Thread


class MultiThreadDownloader:

    __base_headers__ = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    @classmethod
    def headers(cls, extend: [dict, None]):
        if not extend:
            return cls.__base_headers__
        return {**cls.__base_headers__, **extend}

    @staticmethod
    def proxies(host: str):
        if not host:
            return {}
        return {"http": host, "https": host}

    @staticmethod
    def get_file_name(url: str):
        return url.split("?")[0].split("/")[-1]

    @classmethod
    def download_chunk(cls, url: str, header: dict, proxy: str, start: int, end: int, total_bar: tqdm):
        filename = cls.get_file_name(url)
        req_headers = {
            'Range': f'bytes={start}-{end}',
            **cls.headers(header)
        }
        response = requests.get(url, headers=req_headers, proxies=cls.proxies(proxy), stream=True)
        if response.status_code in [200, 206]:
            with open(filename, 'r+b') as f:
                f.seek(start)
                for data in response.iter_content(chunk_size=1024):
                    if data:
                        size = f.write(data)
                        total_bar.update(size)

    @classmethod
    def download(cls, url: str, save_path: str, num_threads: int = 4, proxy: str = None, headers: str = None):
        file_name = cls.get_file_name(url)
        response = requests.get(url, headers=cls.headers(headers), stream=True, proxies=cls.proxies(proxy))
        file_size = int(response.headers.get('content-length', 0))
        chunk_size = file_size // num_threads
        save_to = (Path(save_path) / file_name).absolute()
        with open(save_to, 'wb') as f:
            f.seek(file_size - 1)
            f.write(b'\0')
        total_bar = tqdm(
            total=file_size, unit='B', unit_scale=True, desc=f"文件{file_name}下载进度", position=0, leave=True
        )
        threads = []
        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size - 1 if i < num_threads - 1 else file_size
            thread = Thread(
                target=cls.download_chunk, args=(url, headers, proxy, start, end, file_name, total_bar), daemon=True
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total_bar.close()


if __name__ == '__main__':
    proxy = "http://127.0.0.1:10809"
    download_url = "https://some.source.com/test.txt"
    MultiThreadDownloader.download(url=download_url, save_path='./', num_threads=16)
