NAME=abeja-sdk

requirements.txt: Pipfile.lock
	pipenv lock -r | grep -v '^-i' > requirements.txt

install: clean requirements.txt
	pipenv run python setup.py build
	pipenv run python setup.py install --force

uninstall:
	pip uninstall $(NAME)

clean: requirements.txt
	pipenv run python setup.py clean

dist: clean requirements.txt
	pip install wheel==0.31.1
	pipenv run python setup.py bdist_wheel --universal

lint:
	pipenv run flake8 abeja tests --ignore=E501

test: requirements.txt lint
	pipenv run pytest tests/${TEST_TARGET} --doctest-modules --cov=abeja

integration_test:
	pipenv run pytest -vs integration_tests

fmt:
	pipenv run autopep8 -i -r abeja tests --max-line-length=120

docs:
	sphinx-build -M html doc/source doc/build

release: dist
	twine upload ./dist/abeja_sdk-*-py2.py3-none-any.whl
