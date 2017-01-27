test:
	python -m unittest discover -s "tests/py2/unit" -p "test_*.py"

test-all:
	python -m unittest discover -s "tests/py2" -p "test_*.py"
	python3 -m unittest discover -s "tests/py3" -p "test_*.py"

coverage:
	coverage run -m unittest discover -s "tests/unit" -p "test_*.py"
	coverage html --include="pycdi/*,examples/*"

coverage-all: coverage
	coverage run -m unittest discover -s "tests/" -p "test_*.py"
	coverage html --include="pycdi/*,examples/*"
	python -mwebbrowser htmlcov/index.html &

public:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

public-test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

clean:
	rm -f $(shell find . -name "*.pyc")
	rm -rf htmlcov/ coverage.xml .coverage
	rm -rf dist/ build/
	rm -rf *.egg-info