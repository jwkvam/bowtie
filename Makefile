all: test

test:
	py.test --cov=./ --pylint --pylint-rcfile=pylintrc --pylint-error-types=WCREF --ignore=doc

loop:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=WCREF -f --ignore=doc

debug:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=WCREF -s --pdb --ignore=doc

upload:
	flit wheel --upload
