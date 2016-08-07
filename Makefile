#
PIP = env/bin/pip
PYT = env/bin/python
PY3 = $(shell which python3)

help:
	@echo "install      Install virtualenv and deps"
	@echo "venv         Setup the virtual environment"
	@echo "deps         Run the setup.py dependencies"
	@echo "clean        Cleanup the venv and deps"

install: venv deps

venv:
	rm -rf env
	pip install --upgrade pip
	pip install --upgrade virtualenv
	virtualenv --python=$(PY3) env
	$(PIP) install --upgrade pip

deps:
	$(PIP) install --upgrade -r requirements.txt

clean:
	rm -rf .tox/
	rm -rf build
	rm -rf dist
	rm -rf env
	rm -rf soccerbot.egg-info
	rm *.xml

.PHONY : help install venv deps develop clean
