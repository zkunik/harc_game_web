FROM python:3.9.0
WORKDIR /app
RUN ["pip", "install", "virtualenv"]
COPY Makefile requirements.txt ./
RUN ["make", "venv"]
COPY . .
RUN ["make", "dev-prepare"]
CMD ["make", "run"]
