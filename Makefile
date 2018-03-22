tests: lint test doctest

test:
	coverage run --source topos setup.py test && coverage report

test_travis: test
	coveralls

lint:
	flake8 topos/

livedocs:
	cd docs && make live

docs:
	cd docs && make html

linkcheck:
	cd docs && make linkcheck

doctest:
	cd docs && make doctest &&  cd ..

.PHONY: docs
