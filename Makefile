.PHONY: tests

tests:
	@python -m unittest discover tests/ -p 'test*'

setup:
	@pip install -r requirements.txt

start:
	@python -m wormhole.server

run:
	@docker build . -t wormhole-app
	@docker run wormhole-app
