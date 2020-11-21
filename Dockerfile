FROM python:3.9.0-alpine
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN apk add make
COPY Makefile requirements.txt ./
RUN make venv
COPY . .
