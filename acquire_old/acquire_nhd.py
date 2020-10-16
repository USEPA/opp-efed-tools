import urllib.request
import urllib.error
from params import nhd_regions, vpus_nhd
import os
import re
import string

overwrite = False
zipped_dir = r"E:\zipped\nhd"


def check_path(local_path):
    if os.path.exists(local_path):
        return True
    for a in string.ascii_lowercase:
        path = local_path.format(a)
        if os.path.exists(path):
            return True
    return False


# TODO - capitalization (Hydrodem vs HydroDem), inconsistent paths
def pull_file(region, table, letteral, overwrite=False, verbose=False):
    def grab(url, local):
        try:
            urllib.request.urlretrieve(url, local)
            return True
        except urllib.error.HTTPError:
            if verbose:
                print("Unable to download")

    vpu = vpus_nhd[region]
    if letteral:
        super_region = re.match("(\d{2})", region).group(1)
        filename = f"NHDPlusV21_{vpu}_{region}_{super_region}{{}}_{table}"  # letter, trailing number
    else:
        filename = f"NHDPlusV21_{vpu}_{region}_{table}"
    local_path = os.path.join(zipped_dir, filename + ".7z")
    exists = check_path(local_path)
    if overwrite or not exists:
        for letter in string.ascii_lowercase[:10]:
            l = local_path.format(letter) if letteral else local_path
            print(f"Searching for {l}...")
            for n in range(1, 20):
                root_a = f"https://s3.amazonaws.com/edap-nhdplus/NHDPlusV21/Data/NHDPlus{vpu}"
                root_b = f"https://s3.amazonaws.com/edap-nhdplus/NHDPlusV21/Data/NHDPlus{vpu}/NHDPlus{region}"
                for root in root_a, root_b:
                    trailing_num = str(n).zfill(2)
                    basename = filename.format(letter) if letteral else filename
                    file_url = f"{root}/{basename}_{trailing_num}.7z"
                    found = grab(file_url, l)
                    if found:
                        print(f"Acquired {l}")
                        return
        print(f"Unable to find {filename}")


files = \
    [["CatSeed", True],
     ["FdrFac", True],
     ["FdrNull", True],
     ["FilledAreas", True],
     ["HydroDem", True],
     ["NEDSnapshot", True],
     ["EROMExtension", False],
     ["NHDPlusAttributes", False],
     ["NHDPlusBurnComponents", False],
     ["NHDPlusCatchment", False],
     ["NHDSnapshotFGDB", False],
     ["NHDSnapshot", False],
     ["VPUAttributeExtension", False],
     ["VogelExtension", False],
     ["WBDSnapshot", False]]

nhd_regions = ['07'] + [r for r in nhd_regions if r != '07']
for region in nhd_regions:
    for table, letteral in files:
        pull_file(region, table, letteral)
