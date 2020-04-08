#!/bin/bash

set -ue
NEW_VERSION=${1}
echo "bumping version to ${NEW_VERSION}"
sed -i -e "s/^version.*$/version = \"${NEW_VERSION}\"/g" pyproject.toml
echo "VERSION = \"${NEW_VERSION}\"" > abeja/version.py
echo "complete bumping version to ${NEW_VERSION}"