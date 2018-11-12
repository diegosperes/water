setup:
	@pip install -r requirements.txt

start:
	@python -m water.server

run:
	@docker build . -t water-app
	@docker run water-app
