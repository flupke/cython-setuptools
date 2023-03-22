test:
	pytest

upload:
	rm -rf dist
	./setup.py sdist
	twine upload dist/*
