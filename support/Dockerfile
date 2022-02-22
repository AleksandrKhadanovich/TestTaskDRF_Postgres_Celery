FROM python:3.9

ENV PYTHONUNBUFFERED 1


RUN mkdir /support
WORKDIR /support
COPY . /support/

RUN pip install --upgrade pip

#COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt


CMD ["python", "manage.py", "makemigration","migrate", "runserver", "127.0.0.1:8000"]
#EXPOSE 8000
