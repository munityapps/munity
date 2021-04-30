FROM python:3.9.4

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y postgresql-client
RUN apt-get install -y libffi-dev
RUN apt-get install -y gcc

COPY ./plugins /usr/src/plugins/

RUN /usr/local/bin/python -m pip install --upgrade pip

# REQUIREMENTS
COPY ./api/requirements.txt /requirements_all.txt
RUN pip install --requirement /requirements_all.txt

# COPY CODE
COPY /api /usr/src/app

# Plugins install deps
COPY ./configurations/api/runplugins.sh /docker-entrypoint.d/10-runplugins.sh
RUN chmod +x /docker-entrypoint.d/10-runplugins.sh