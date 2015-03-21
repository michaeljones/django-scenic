
test:
	flake8 scenic
	flake8 tests/project
	cd tests/project; python manage.py test
	nosetests tests
