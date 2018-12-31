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
		@echo -e "$(COLOUR_YELLOW)make test$(COLOUR_NONE) : Run the test suite (using feedbackdb/uktrade as db/usr/pass"
		@echo -e "$(COLOUR_YELLOW)make sdist$(COLOUR_NONE) : Rebuild the last version"

test:
		$(VENV_PATH)/python ./runtests.py feedbackdb uktrade uktrade

sdist:
		rm dist/*.tar.gz;
		python setup.py sdist;
