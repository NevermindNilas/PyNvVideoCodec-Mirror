# PyNvVideoCodec Mirror

This repository is an automated mirror of the [PyNvVideoCodec](https://pypi.org/project/PyNvVideoCodec/) package from PyPI.

> [!IMPORTANT]
> **Use at your own risk.** This is an unofficial mirror maintained for convenience and automation purposes. It is not affiliated with the original authors of `PyNvVideoCodec`.

## How it Works

This repository is automatically updated once a week via GitHub Actions.

1. **Detection**: The workflow checks PyPI for the latest version of `PyNvVideoCodec`.
2. **Synchronization**: If a new version is detected:
   - The script downloads the source distribution (`sdist`) or the most compatible wheel.
   - It extracts the contents into the root of this repository.
   - It preserves repository-specific files (e.g., `.git`, `.github`, `.gitignore`, and the sync script).
3. **Tagging**: Each synced version is committed and tagged with the corresponding PyPI version number.

## Update Frequency

The synchronization workflow runs **every Sunday at midnight (UTC)**. You can also trigger a manual sync via the "Actions" tab if a new release is urgently needed.

## Repository Structure

- `.github/workflows/mirror.yml`: The GitHub Actions workflow definition.
- `sync_pypi.py`: The Python script responsible for fetching and extracting the package.
- `README.md`: This file.
- **Root Directory**: Contains the extracted source code/files from the latest PyPI release.

## Warnings

> [!WARNING]
> **Not the Source of Truth**: Always refer to the official [PyPI page](https://pypi.org/project/PyNvVideoCodec/) or official NVIDIA documentation for the most accurate and up-to-date information regarding this package.

> [!CAUTION]
> **Automated Extraction**: The synchronization process uses automated extraction. While it attempts to handle `sdist` and wheels correctly, structure changes in future versions of the package may require updates to the `sync_pypi.py` script.

> [!NOTE]
> This mirror only tracks releases published on PyPI. It does not contain development branches or unreleased code.

## License

This mirroring tool is provided under the same license as the original `PyNvVideoCodec` package (where applicable). Please check the extracted files for specific licensing details from NVIDIA.
