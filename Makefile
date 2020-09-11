.PHONY: test

test:
	pytest -xv videocapture.py test.py

install:
	python3 -m pip install -r requirements.txt
