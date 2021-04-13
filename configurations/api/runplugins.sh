#!/bin/sh

set -x
set -e

cp /usr/src/app/requirements.txt /requirements_all.txt
find ../plugins -name requirements.txt | xargs cat > /requirements_all.txt
cat /requirements_all.txt
pip install --requirement /requirements_all.txt

exec "$@"
