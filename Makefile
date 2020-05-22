NAME=abeja-sdk

.PHONY: clean
clean:
	rm -rf dist

.PHONY: dist
dist: clean
	pip install wheel==0.31.1
	poetry build -f wheel

.PHONY: lint
lint:
	poetry run flake8 abeja tests

.PHONY: mypy
mypy:
	poetry run mypy --config-file .mypy.ini \
	--package abeja.common \
	--package abeja.train \
	--package abeja.training \
	--package tests.common \
	--package tests.training

.PHONY: test
test: lint mypy
	poetry run pytest tests/${TEST_TARGET} --doctest-modules --cov=abeja

.PHONY: integration_test
integration_test:
	poetry run pytest -vs integration_tests

.PHONY: fmt format
fmt: format

format:
	poetry run autopep8 -r --in-place --aggressive --aggressive abeja tests

.PHONY: docs
docs:
	poetry run sphinx-build -M html doc/source doc/build

.PHONY: release
release: dist
	poetry publish -u ${TWINE_USERNAME} -p ${TWINE_PASSWORD}
