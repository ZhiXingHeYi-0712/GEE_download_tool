
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import requests
import os
from pathlib import Path

class DownloadPool():
    def __init__(self, max_workers_count) -> None:
        self.executor = ThreadPoolExecutor(max_workers_count)
        self.futures = []

    def submit(self, download_url, download_path, file_name):
        f = self.executor.submit(self.directDownload, download_url, download_path, file_name)
        self.futures.append(f)

    def directDownload(self, download_url, download_path, file_name):
        content = requests.get(download_url, allow_redirects=True).content

        if not (Path(download_path).exists() and Path(download_path).is_dir()):
            # path does not exist
            os.mkdir(download_path)

        with open(os.path.join(download_path, f'{file_name}.zip'), 'wb') as f:
            f.write(content)

    def wait(self):
        wait(self.futures)