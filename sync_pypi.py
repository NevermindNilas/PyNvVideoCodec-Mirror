import os
import requests
import json
import subprocess
import shutil
import zipfile
import tarfile
from io import BytesIO

PACKAGE_NAME = "PyNvVideoCodec"
PYPI_URL = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"

def get_latest_pypi_version():
    response = requests.get(PYPI_URL)
    response.raise_for_status()
    data = response.json()
    return data["info"]["version"], data["releases"][data["info"]["version"]]

def download_and_extract(url, target_dir):
    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    # Clear target directory except for git-related files and the script itself
    for item in os.listdir(target_dir):
        if item in [".git", ".github", "sync_pypi.py", ".gitignore"]:
            continue
        path = os.path.join(target_dir, item)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    content = BytesIO(response.content)
    if url.endswith(".whl") or url.endswith(".zip"):
        with zipfile.ZipFile(content) as z:
            z.extractall(target_dir)
    elif url.endswith(".tar.gz"):
        with tarfile.open(fileobj=content, mode="r:gz") as t:
            t.extractall(target_dir)
            # Tarballs often have a nested directory
            # If there's only one directory in the extraction, move its contents up
            # (Skipping advanced logic for now, usually sdist structure is predictable)
    
    print("Extraction complete.")

def main():
    version, release_files = get_latest_pypi_version()
    print(f"Latest PyPI version: {version}")
    
    # Check if we already have this version handled via git tag
    try:
        current_tags = subprocess.check_output(["git", "tag"], text=True).splitlines()
    except subprocess.CalledProcessError:
        current_tags = []

    if version in current_tags:
        print(f"Version {version} already exists in repo tags. Skipping.")
        return

    # Find best file to download
    # Prefer sdist, then manylinux wheel, then win_amd64 wheel (just for source accessibility)
    best_file = None
    for f in release_files:
        if f["packagetype"] == "sdist":
            best_file = f
            break
    
    if not best_file:
        # Fallback to wheel
        for f in release_files:
            if "manylinux" in f["filename"] and "x86_64" in f["filename"]:
                best_file = f
                break
        if not best_file:
            best_file = release_files[0] # Take whatever is there

    download_and_extract(best_file["url"], ".")
    
    # Commit changes
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"])
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Sync version {version} from PyPI"])
    subprocess.run(["git", "tag", version])
    
    # We don't push here, the GHA workflow will push tags and master
    print(f"Updated to {version} and tagged.")

if __name__ == "__main__":
    main()
