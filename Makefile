# Makefile for Python Project

# Variables
PYTHON = python
PIP = pip
PROJECT_NAME = your_project_name
TEST_DIR = tests

# Targets and Rules
.PHONY: install test clean

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest $(TEST_DIR)

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;

push:
	git add .
	@read -p "Enter commit message: " commit_message; \
	git commit -m "$$commit_message"
	git push