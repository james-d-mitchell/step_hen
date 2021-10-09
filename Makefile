tests:
	tox -- -x tests/

.PHONY: tests


coverage:
	@coverage run --source . --omit="tests/*" -m py.test
	@coverage html
	@echo "See: htmlcov/index.html"


doc: 
	@cd docs && make html

clean-doc:
	rm -rf docs/build

clean: clean-doc
	rm -rf *.egg-info 
	rm -rf docs/build
	rm -rf build/
	rm -rf __pycache__/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf *.egg-info
	rm -rf .tox
	rm -rf tests/__pycache__
	rm -rf step_hen/__pycache__

lint: 
	pylint step_hen/*.py
