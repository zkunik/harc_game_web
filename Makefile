VENV_NAME = venv
VENV_ACTIVATE_PATH = $(VENV_NAME)/bin/activate
PROJECT_DIR = harc_game_web

venv:
	python3 -m virtualenv ./$(VENV_NAME)
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m pip install -r requirements.txt

dev-migrate: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py makemigrations && \
	python3 $(PROJECT_DIR)/manage.py migrate

dev-populate-db-examples: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py loaddata example_db.json --app teams && \
	python3 $(PROJECT_DIR)/manage.py loaddata example_db.json --app users && \
	python3 $(PROJECT_DIR)/manage.py loaddata example_db.json --exclude teams --exclude users

dev-prepare: dev-migrate dev-populate-db-examples

populate-db: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 utils/convert_tasks.py $(PROJECT_DIR)/apps/tasks/fixtures/base_db.csv && \
	python3 utils/convert_passwords.py $(PROJECT_DIR)/apps/wotd/fixtures/base_db.csv && \
	python3 $(PROJECT_DIR)/manage.py loaddata base_db.json

prepare: dev-migrate populate-db

run: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py runserver 0.0.0.0:8000

test: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py test harc_game_web

shell: venv
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 $(PROJECT_DIR)/manage.py shell

clean-media:
	rm -rf $(PROJECT_DIR)/media/

clean-db:
	find harc_game_web/ -type f | grep migrations | (grep -v __init__.py || echo :) | xargs rm && \
	rm -f $(PROJECT_DIR)/db.sqlite3

clean: clean-media clean-db
