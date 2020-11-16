VENV_NAME = venv
VENV_ACTIVATE_PATH = $(VENV_NAME)/bin/activate
PROJECT_DIR = harc_game_web

venv:
	python3 -m virtualenv ./$(VENV_NAME)
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m pip install pip --upgrade && \
	python3 -m pip install -r requirements.txt

dev-migrate: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py makemigrations && \
	python3 $(PROJECT_DIR)/manage.py migrate

dev-populate-db-examples: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py loaddata example_db.json

dev-prepare: dev-migrate dev-populate-db-examples

run: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py runserver 0.0.0.0:8000

test: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py test harc_game_web

clean-media:
	rm -rf $(PROJECT_DIR)/media/

clean-db:
	find harc_game_web/ -type f | grep migrations | grep -v __init__.py | xargs -r rm && \
	rm -f $(PROJECT_DIR)/db.sqlite3

clean: clean-media clean-db