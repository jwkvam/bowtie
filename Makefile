all: test

test:
	py.test --cov=./ --pylint --pylint-rcfile=pylintrc --pylint-error-types=EF --ignore=doc

coverage:
	py.test --cov=./ --cov-report html --ignore=doc

loop:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=EF -f --ignore=doc

debug:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=EF -s --pdb --ignore=doc

upload:
	flit wheel --upload
