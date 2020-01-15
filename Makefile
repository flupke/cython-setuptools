test:
	pytest -m "not slow"

test_all:
	pytest

upload:
	rm -rf dist
	./setup.py sdist
	twine upload dist/*
