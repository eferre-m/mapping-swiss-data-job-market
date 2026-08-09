VENV        := .venv
PYTHON      := $(VENV)/bin/python3
PIP         := $(VENV)/bin/pip
FLAKE8      := $(VENV)/bin/flake8
MYPY        := $(VENV)/bin/mypy

SRCDIR      := src

INPUT       := offer_raw_test.json

RM          := rm -rf

# -------------------------------------------------------------------------- #

# Default target: running bare "make" just runs the quality checks.
all: check

# Creates the virtual environment if it doesn't exist yet, and installs
# the tools this project needs (flake8, mypy) straight into it, so that
# .venv/bin/flake8 and .venv/bin/mypy are ready to use.
# NOTE: "source .venv/bin/activate" can't live inside a Makefile recipe,
# since each recipe line runs in its own subshell and the activation would
# be lost right away. Activate it yourself when working interactively:
#   source .venv/bin/activate
venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy

# Runs the parser, using the virtual environment's python.
parse:
	$(PYTHON) -m src.parse $(INPUT)

# Checks source code style with flake8.
lint:
	$(FLAKE8) $(SRCDIR)

# Checks static types with mypy.
typecheck:
	$(MYPY) $(SRCDIR)

# Runs all code quality checks at once.
check: lint typecheck

# Removes generated caches (Python and tool caches).
# Does not delete any data or source code files.
clean:
	find $(SRCDIR) -type d -name "__pycache__" -exec $(RM) {} +
	$(RM) .mypy_cache

# Full clean: everything clean does, plus removes the virtual environment.
fclean: clean
	$(RM) $(VENV)

# Rebuilds everything from scratch: wipes the venv, recreates it, and
# reruns the checks. Useful after dependency or interpreter issues.
re: fclean venv all

.PHONY: all venv parse lint typecheck check clean fclean re