import os
import zipfile
import time
from params import nhd_regions
import pandas as pd
from paths import local_path, remote_path, zipped_path, combinations_path

years = list(range(2015, 2020))


def zipped_paths(name):
    local_zipfile = os.path.join(local_path, zipped_path, f"{name}.zip")
    remote_zipfile = os.altsep.join((remote_path, zipped_path, f"{name}.zip"))
    return local_zipfile, remote_zipfile


def compress_files(zipfile_path, contents):
    start = time.time()
    file = zipfile.ZipFile(zipfile_path, "w")
    for item in contents:
        print(f"Adding {item} to {zipfile_path}...")
        try:
            file.write(item, os.path.basename(item), zipfile.ZIP_DEFLATED)
        except FileNotFoundError:
            print(f"File {item} doesn't exist")
    print(f"Finished in {int(time.time() - start)} seconds")


local_z, remote_z = zipped_paths("Combinations")
local_combos = [os.path.join(local_path, combinations_path).format(r, y) for r in nhd_regions for y in years]
local_combos = [os.path.join(local_path, combinations_path).format('01', '2017')]
compress_files(local_z, local_combos)