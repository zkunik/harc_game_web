FROM python:3.9.0
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN ["python", "harc_game_web/manage.py", "makemigrations"]
RUN ["python", "harc_game_web/manage.py", "migrate"]
RUN ["python", "harc_game_web/manage.py", "loaddata", "example_db.json"]
CMD ["python", "harc_game_web/manage.py", "runserver", "0.0.0.0:8000"]
