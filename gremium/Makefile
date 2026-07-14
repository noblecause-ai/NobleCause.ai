.PHONY: session install test

# Beispiel:
#   make session QUESTION="Welche drei Interventionen …?" TITLE="Eröffnungsfrage"
session:
	python3 run_session.py --question "$(QUESTION)" --title "$(TITLE)"

install:
	pip3 install -r requirements.txt

test:
	python3 -m pytest tests/ -q
