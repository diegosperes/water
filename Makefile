.PHONY: tests

tests:
	@python -m unittest discover tests/ -p 'test*'

setup:
	@pip install -r requirements.txt

start:
	@python -m water.server

run:
	@docker build . -t water-app
	@docker run water-app
