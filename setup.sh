#!/usr/bin/env bash

REPO_URL=https://api.github.com/repos/mozilla/geckodriver/releases/latest
FILE_EXTENSION=".tar.gz"
SUPPORTED_OS=("win" "linux" "macos")

usage() {
    printf "\nUsage: %s [-s <string>] [-v <32|64>]" "${0}"; exit 1;
}

while getopts ":hs:v:" option; do
    case "${option}" in
        s) OS=${OPTARG};;
        v) VERSION=${OPTARG}
        (( VERSION == 32 || VERSION == 64 )) || usage;;
        h | *) usage;;
    esac
done

# Check if specified os is supported by developer team and get filename
if [[ ${OS} =~ ^SUPPORTED_OS$ ]]; then
    printf "Error: ${OS} is not in %s" "${SUPPORTED_OS[@]}";
    exit 1;
elif [[ "${OS}" == "macos" ]]; then
    OS="${OS}";
else
    OS="${OS}${VERSION}";
fi

# Create folder for temporary files
if [ ! -d ./.cache ]; then
    mkdir -p ./.cache;
fi

# Get and download arhcive with required file
curl -s $REPO_URL \
| grep "browser_download_url.*${OS}${FILE_EXTENSION}" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -i - -P ./.cache

# Unpack geckodriver to root dir
tar -xvzf ./.cache/*"$OS".tar.gz

# Remove temporary files
rm -r ./.cache

# Make geckodriver executable
chmod +x ./geckodriver
