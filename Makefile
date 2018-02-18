tests: lint test doctest

test:
	coverage run --source topos setup.py test && coverage report

test_travis: test
	coveralls

lint:
	flake8 topos/

doctest:
	cd docs && make doctest &&  cd ..
