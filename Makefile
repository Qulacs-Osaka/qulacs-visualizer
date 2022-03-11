PYTEST := poetry run pytest
FORMATTER := poetry run black
LINTER := poetry run flake8
IMPORT_SORTER := poetry run isort
TYPE_CHECKER := poetry run mypy
SPHINX_APIDOC := poetry run sphinx-apidoc

PROJECT_DIR := qulacsvis
CHECK_DIR := $(PROJECT_DIR) tests
PORT := 8000

GENERATE_SCRIPT_DIR := tests/generate
USE_LATEX?=no

ifeq "$(USE_LATEX)" "yes"
	PYTEST_OPT_LATEX=--runlatex
else
	PYTEST_OPT_LATEX=
endif

# If this project is not ready to pass mypy, remove `type` below.
.PHONY: check
check: format lint type

.PHONY: ci
ci: format_check lint type

.PHONY: test
test:
	$(PYTEST) -v --mpl $(PYTEST_OPT_LATEX)

tests/%.py: FORCE
	$(PYTEST) $@

# Idiom found at https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:

.PHONY: format
format:
	$(FORMATTER) $(CHECK_DIR)
	$(IMPORT_SORTER) $(CHECK_DIR)

.PHONY: format_check
format_check:
	$(FORMATTER) $(CHECK_DIR) --check --diff
	$(IMPORT_SORTER) $(CHECK_DIR) --check --diff

.PHONY: lint
lint:
	$(LINTER) $(CHECK_DIR)

.PHONY: type
type:
	$(TYPE_CHECKER) $(CHECK_DIR)

.PHONY: serve
serve: html
	poetry run python -m http.server --directory doc/build/html $(PORT)

.PHONY: doc
html: api
	poetry run $(MAKE) -C doc html

.PHONY: api
api:
	$(SPHINX_APIDOC) -f -e -o doc/source $(PROJECT_DIR)

.PHONY: gen-text
gen-text:
	poetry run python $(GENERATE_SCRIPT_DIR)/text_correct_data.py

.PHONY: gen-latex
gen-latex:
ifeq "$(USE_LATEX)" "yes"
	@make gen-hashlib
	poetry run python $(GENERATE_SCRIPT_DIR)/latex_correct_data.py
else
	@echo "LaTeX is not enabled in Makefile. Use 'make gen-latex USE_LATEX=yes' to enable."
endif

.PHONY: gen-latex-source
gen-latex-source:
	poetry run python $(GENERATE_SCRIPT_DIR)/latex_source_correct_data.py

.PHONY: gen-mpl
gen-mpl: gen-hashlib
	poetry run python $(GENERATE_SCRIPT_DIR)/mpl_correct_data.py

.PHONY: gen-hashlib
gen-hashlib:
	poetry run python $(GENERATE_SCRIPT_DIR)/print_hashlib_filename.py \
	 | xargs -I{} poetry run pytest --mpl-generate-hash-library={} $(PYTEST_OPT_LATEX)
