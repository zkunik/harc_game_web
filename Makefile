VENV_NAME = venv
VENV_ACTIVATE_PATH = $(VENV_NAME)/bin/activate
PROJECT_DIR = harc_game_web

venv:
	python3 -m virtualenv ./$(VENV_NAME)
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m pip install pip --upgrade && \
	python3 -m pip install -r requirements.txt

dev-prepare: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py makemigrations && \
	python3 $(PROJECT_DIR)/manage.py migrate

run: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py runserver

test: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py test
