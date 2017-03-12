all: clean dist

clean:
	@rm -rf build dist
	@find . -name "*.pyc" -delete
.PHONY: clean

distclean:
	@git clean -xdf
.PHONY: distclean

# Setuptools
sdist:
	@python setup.py sdist

bdist_wheel:
	@python setup.py bdist_wheel

dist: sdist bdist_wheel

install:
	@python setup.py install

# PyPI and TestPyPI
release: clean dist
	@twine upload dist/* -s -i $(IDENTITY)

test_release: clean dist
	@twine upload dist/* -r testpypi --skip-existing -s -i $(IDENTITY)

# Sphinx documentation
docs: clean
	@tox -r -e docs
