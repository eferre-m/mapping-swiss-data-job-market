VENV        := .venv
PYTHON      := $(VENV)/bin/python3
PIP         := $(VENV)/bin/pip
FLAKE8      := $(VENV)/bin/flake8
MYPY        := $(VENV)/bin/mypy

SRCDIR      := src 

INPUT       := offer_raw_test.json

RM          := rm -rf

# -------------------------------------------------------------------------- #

all: check

#   source .venv/bin/activate
venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requierements.txt

# Runs the parser, using the virtual environment's python.
parse:
	$(PYTHON) -m src.parse $(INPUT)

# Requires DATABASE_URL to be set, e.g.:
# 	export DATABASE_URL=postgresql://user:pass@localhost:5432/jobs
db-init:
	psql "$(DATABASE_URL)" -f sql/schema.sql

# Checks source code style with flake8.
lint:
	$(FLAKE8) $(SRCDIR)

# Checks static types with mypy.
typecheck:
	$(MYPY) $(SRCDIR)

# Runs all code quality checks at once.
check: lint typecheck

# Removes generated caches (Python and tool caches).
clean:
	find $(SRCDIR) -type d -name "__pycache__" -exec $(RM) {} +
	$(RM) .mypy_cache

.PHONY: all venv parse lint typecheck check 