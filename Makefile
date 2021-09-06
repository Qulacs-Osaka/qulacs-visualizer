PYTEST := poetry run pytest -v
PYSEN := poetry run pysen

.PHONY: test
test:
	$(PYTEST)

.PHONY: lint
lint:
	$(PYSEN) run lint

.PHONY: format
format:
	$(PYSEN) run format

.PHONY: check
check: format lint