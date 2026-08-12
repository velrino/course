.PHONY: validate test-labs docs serve

PYTHON ?= python3

validate:
	$(PYTHON) scripts/validate_course.py

test-labs:
	$(PYTHON) labs/run-all-tests.py

docs: validate
	mkdocs build --strict

serve:
	mkdocs serve
