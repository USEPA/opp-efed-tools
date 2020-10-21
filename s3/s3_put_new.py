import os
import zipfile
import time
from params import nhd_regions
import boto3
from s3_lib import upload_file
from paths import local_path, remote_path, zipped_path, combinations_path

session = boto3.session.Session(profile_name='sam')
c = session.get_credentials()
s3 = session.resource('s3')
sam_staged_bucket = s3.Bucket('sam-staged-inputs')

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
        file.write(item, os.path.basename(item), zipfile.ZIP_DEFLATED)
    print(f"Finished in {int(time.time() - start)} seconds")


def compress_combinations():
    local_z, remote_z = zipped_paths("Combinations")
    local_combos = [os.path.join(local_path, combinations_path).format(r, y) for r in nhd_regions for y in years]
    # Need to check for overwrite here
    if False:
        compress_files(local_z, local_combos)
    else:
        print("Skipping compression")

    upload_file(local_z, f"public/{os.path.basename(local_z)}")

compress_combinations()