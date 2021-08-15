tests:
	tox -- -x tests/

.PHONY: tests


coverage:
	@coverage run --source . --omit="tests/*" -m py.test
	@coverage html
	@echo "See: htmlcov/index.html"


doc: 
	@cd docs && make html

clean:
	rm -rf docs/build

lint: 
	pylint stephen/*.py
