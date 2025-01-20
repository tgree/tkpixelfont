# Copyright (c) 2025 by Terry Greeniaus.
MODULE      := tkpixelfont
MODULE_VERS := 0.1.0
MODULE_DEPS := \
		setup.cfg \
		setup.py \
		tkpixelfont/geom/*.py \
		tkpixelfont/tk/*.py \
		tkpixelfont/*.py \

FLAKE_MODULES := tkpixelfont
LINT_MODULES  := tkpixelfont
WHEEL_PATH    := dist/$(MODULE)-$(MODULE_VERS)-py3-none-any.whl
TGZ_PATH      := dist/$(MODULE)-$(MODULE_VERS).tar.gz

.PHONY: all
all: test packages

.PHONY: clean
clean:
	rm -rf dist $(MODULE).egg-info build
	find . -name "*.pyc" | xargs rm
	find . -name __pycache__ | xargs rm -r

.PHONY: test
test: flake8 lint unittest

.PHONY: flake8
flake8:
	python3 -m flake8 $(FLAKE_MODULES)

.PHONY: lint
lint:
	pylint -j2 $(LINT_MODULES)

.PHONY: unittest
unittest:
	python3 -m unittest

.PHONY: install
install: $(WHEEL_PATH) | uninstall
	sudo python3 -m pip install $(WHEEL_PATH)

.PHONY: uninstall
uninstall:
	sudo python3 -m pip uninstall $(MODULE)

.PHONY: packages
packages: $(WHEEL_PATH)

.PHONY: publish
publish: all
	python3 -m twine upload $(WHEEL_PATH) $(TGZ_PATH)

$(WHEEL_PATH): $(MODULE_DEPS) Makefile
	python3 -m build
	python3 -m twine check $@
