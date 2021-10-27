#!/bin/bash

set -e
set -x

# Cleaning all packages
rm -rf lib

# Building js files from TS
npx tsc

# Copy package json
cp package.json ./lib

# Copy assets
cp -rf ./src/assets ./lib

# Copy translations
cp -rf ./src/translations ./lib

# Copy all SCSS resources
rsync -armv --include="*/" --include="*.scss" --exclude="*" ./src/* ./lib

# Publish !~~~~~~~
npm publish ./lib