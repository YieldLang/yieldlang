.PHONY : docs
docs :
	rm -rf docs/build/
	rm -rf docs/source/autoapi/
	sphinx-autobuild -b html --watch yieldlang/ docs/source/ docs/build/

.PHONY : run-checks
run-checks :
	isort --check .
	black --check .
	ruff check .
	mypy .
	CUDA_VISIBLE_DEVICES='' pytest -v --color=yes --doctest-modules tests/ yieldlang/

.PHONY : build
build :
	rm -rf *.egg-info/
	python -m build
