import os
import urllib.request
import zipfile
from paths import local_path, remote_path

def download_file(filename):
    local = os.path.join(local_path, filename)
    remote = urllib.parse.urljoin(remote_path, filename)
    print(type(remote))
    print(remote)
    print(f"Downloading {remote} to {local}...")
    urllib.request.urlretrieve(remote, local)


if not os.path.isdir(local_path):
    os.makedirs(local_path)

download_file(combinations_file)
