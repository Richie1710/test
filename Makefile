.PHONY: test build

test:
	python -m unittest discover

build:
	docker build -t merge-request-image .
