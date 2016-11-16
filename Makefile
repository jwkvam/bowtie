all: test
 

test:
	PYTHONPATH=$(pwd) py.test --cov=./ --pylint --pylint-rcfile=pylintrc --pylint-error-types=EF --ignore=doc

coverage:
	PYTHONPATH=$(pwd) py.test --cov=./ --cov-report html --ignore=doc

loop:
	PYTHONPATH=$(pwd) py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=EF -f --ignore=doc

debug:
	PYTHONPATH=$(pwd) py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=EF -s --pdb --ignore=doc

upload:
	flit wheel --upload
