# Makefile
.PHONY: install run

install:
	pipenv install

run:
	pipenv run python -m src.scrape --expand