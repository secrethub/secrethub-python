import os
import sys
import shutil
import hashlib
import zipfile
import argparse
import tempfile
from collections import defaultdict

import pefile
from machomachomangler.pe import redll

def hash_filename(filepath, blocksize=65536):
    hasher = hashlib.sha256()

    with open(filepath, "rb") as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)

    root, ext = os.path.splitext(filepath)
    return f"{os.path.basename(root)}-{hasher.hexdigest()[:8]}{ext}"

def mangle_filename(old_filename, new_filename, mapping):
    print(old_filename, new_filename, mapping)
    with open(old_filename, "rb") as f:
        buf = f.read()

    new_buf = redll(buf, mapping)

    with open(new_filename, "wb") as f:
        f.write(new_buf)


parser = argparse.ArgumentParser(
    description="Add .dll to wheel."
)
parser.add_argument("WHEEL_FILE", type=str, help="Path to wheel file")
parser.add_argument("DLL", type=str, help="Path to dll.")
parser.add_argument("OUT", type=str, help="Path to output dir.")

args = parser.parse_args()

wheel_name = os.path.basename(args.WHEEL_FILE)
package_name = wheel_name.split("-")[0]
repaired_wheel = os.path.join(args.OUT, wheel_name)

old_wheel_dir = tempfile.mkdtemp()
new_wheel_dir = tempfile.mkdtemp()

with zipfile.ZipFile(args.WHEEL_FILE, "r") as wheel:
    wheel.extractall(old_wheel_dir)
    wheel.extractall(new_wheel_dir)
    pyd_path = list(filter(lambda x: x.endswith(".pyd"), wheel.namelist()))[0]
    tmp_pyd_path = os.path.join(old_wheel_dir, package_name, os.path.basename(pyd_path))

mapping = {}
hashed_name = hash_filename(args.DLL)
mapping[os.path.basename(args.DLL).encode("ascii")] = hashed_name.encode("ascii")
shutil.copy(
    args.DLL,
    os.path.join(new_wheel_dir, package_name, hashed_name),
)

pyd_files = [f for f in os.listdir(os.path.join(old_wheel_dir, package_name)) if os.path.isfile(os.path.join(old_wheel_dir, package_name, f)) and f.endswith(".pyd")]
print(pyd_files)
old_name = os.path.join(old_wheel_dir, package_name, os.path.basename(pyd_files[0]))
new_name = os.path.join(new_wheel_dir, package_name, os.path.basename(pyd_files[0]))
mangle_filename(old_name, new_name, mapping)

with zipfile.ZipFile(repaired_wheel, "w", zipfile.ZIP_DEFLATED) as new_wheel:
    for root, dirs, files in os.walk(new_wheel_dir):
        for file in files:
            new_wheel.write(
                os.path.join(root, file), os.path.join(os.path.basename(root), file)
            )
