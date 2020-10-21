import os

# Parent paths
local_path = r"E:\opp-efed-data"
remote_path = "https://sam-staged-inputs.s3.amazonaws.com/public/"

# Zipped paths
zipped_path = "zipped"

# File directories
combinations_path = os.altsep.join(("scenarios", "Intermediate", "Combinations", "{}_{}.csv"))  # region, year