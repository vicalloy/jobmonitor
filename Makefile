.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

ci:
	pipenv run py.test --junitxml=report.xml

isort:
	isort --recursive lbjobmonitor tests

flake8:
	pipenv run flake8 lbjobmonitor tests

coverage:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report html --cov=lbjobmonitor tests

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
