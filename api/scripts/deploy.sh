#!/bin/bash

set -x
set -e

rm -rf dist/*
python3 -m build
twine upload  dist/* --verbose
