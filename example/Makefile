SHELL := /bin/bash
APPLICATION_NAME="Feed Gov Back"
APPLICATION_VERSION=1.0
VENV_PATH=~/Envs/feed-gov/bin

# Colour coding for output
COLOUR_NONE=\033[0m
COLOUR_GREEN=\033[32;01m
COLOUR_YELLOW=\033[33;01m


.PHONY: help test
help:
		@echo -e "$(COLOUR_GREEN)|--- $(APPLICATION_NAME) [$(APPLICATION_VERSION)] ---|$(COLOUR_NONE)"
		@echo -e "$(COLOUR_YELLOW)make reinstall$(COLOUR_NONE) : Rebuild the lib locally and reinstall it"
		@echo -e "$(COLOUR_YELLOW)make sdist$(COLOUR_NONE) : Run the dev server"

reinstall:
		$(VENV_PATH)/pip uninstall feed-gov-back -y;
		pip install ../dist/feed-gov-back-0.1.tar.gz;

run:
		./manage.py runserver
