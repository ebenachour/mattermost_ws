run_api:
	# Launch uWSGI
	uwsgi --ini uwsgi.ini 

test:
	# run tests
	pytest -vv

coverage:
	pytest --cov --cov-report xml

black:
	# Apply black to all files
	black .

lint:
	# check linters according to black
	flake8