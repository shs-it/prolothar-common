cython :
	python setup.py build_ext --inplace

clean :
	python setup.py clean --all

test :
	python -m coverage erase
	python -m coverage run --branch --source=./prolothar_common -m unittest discover -v
	python -m coverage xml -i

check_requirements :
	safety check -r requirements.txt

package :
	python setup.py sdist bdist_wheel

clean_package :
	rm -R dist build prolothar_common.egg-info

publish :
	twine upload --skip-existing --verbose -u ${PYPI_USER} -p ${secrets.PYPI_PASSWORD} dist/*