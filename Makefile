NAME=abeja-sdk

clean:
	rm -rf dist

dist: clean
	pip install wheel==0.31.1
	poetry build -f wheel

lint:
	poetry run flake8 abeja tests --ignore=E501

test: lint
	poetry run pytest tests/${TEST_TARGET} --doctest-modules --cov=abeja

integration_test:
	poetry run pytest -vs integration_tests

fmt:
	poetry run autopep8 -i -r abeja tests --max-line-length=120

docs:
	poetry run sphinx-build -M html doc/source doc/build

release: dist
	poetry publish -u ${TWINE_USERNAME} -p ${TWINE_PASSWORD}
