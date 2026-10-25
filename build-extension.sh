#!/usr/bin/env bash
#
# Prepares TidyIt for NZBGet v23+ (the Extension Manager):
# - build/TidyIt/ can be copied straight into NZBGet's scripts folder
# - build/tidyit-<version>-dist.zip is the same thing, ready for a release
#
set -euo pipefail

# Always work from the folder this script lives in
cd "$(dirname "$0")"

# Defines the name of the plugin:
NAME=TidyIt
OUT="build/${NAME}"
VERSION=$(python3 -c "import json; print(json.load(open('manifest.json'))['version'])")
# Our output file
ZIP="tidyit-${VERSION}-dist.zip"

# Start fresh
rm -rf build
mkdir -p "${OUT}"

# Copy in the script, the manifest, the docs and the translations
cp -r TidyIt.py manifest.json README.md LICENSE _locales "${OUT}/"

# Install every package TidyIt needs into lib/, picking versions that
# still work on Python 3.8
python3 -m pip install --quiet --disable-pip-version-check --no-compile \
    --target "${OUT}/lib" --python-version 3.8 --only-binary :all: \
    -r requirements.txt

# Remove what TidyIt doesn't need to run:
# - lxml only works on the platform that built it (pynzbget doesn't need it)
# - setuptools is an install tool
# - bin/ holds command line tools made for this machine
(
    cd "${OUT}/lib"
    rm -rf bin lxml lxml-*.dist-info \
        setuptools setuptools-*.dist-info pkg_resources \
        _distutils_hack distutils-precedence.pth
)
find "${OUT}" -name __pycache__ -prune -exec rm -rf {} +

# Remove any compiled files. They only work on the platform that built them,
# and TidyIt's packages are plain Python anyway. This keeps the extension
# working on ARM (Raspberry Pi, most NAS boxes).
find "${OUT}/lib" \( -name '*.so' -o -name '*.pyd' \) -delete

# Zip it up the same way the official extensions are
(cd build && zip -qr "${ZIP}" "${NAME}")

# Write a checksum so people can make sure their download isn't damaged
# (sha256sum on Linux, shasum on macOS)
(
    cd build
    if command -v sha256sum >/dev/null; then
        sha256sum "${ZIP}" > "${ZIP}.sha256"
    else
        shasum -a 256 "${ZIP}" > "${ZIP}.sha256"
    fi
)

echo "Folder:   ${OUT}"
echo "Zip:      build/${ZIP}"
echo "Checksum: build/${ZIP}.sha256"
