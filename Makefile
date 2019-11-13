.PHONY: serve deploy install

install:
	pip install -r requirements.txt

serve:
	mkdocs serve

deploy:
	mkdocs gh-deploy