FROM python:3.9-slim
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt-get install -y libgdal-dev libffi-dev git curl

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /code/

CMD ["python", "manage.py", "runserver", "0:8000"]
