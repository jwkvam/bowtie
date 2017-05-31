all: test

test:
	py.test --cov=./ --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF --ignore=doc

unit:
	py.test --cov=./

lint:
	py.test --pylint -m pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF --ignore=doc

eslint:
	eslint bowtie/src/*.js{,x}

checkdocs:
	pydocstyle --count --match-dir='(?!examples|doc|.*templates)[^\.].*'

coverage:
	py.test --cov=./ --cov-report html --ignore=doc

loop:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF -f --ignore=doc

debug:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF -s --pdb --ignore=doc

upload:
	flit wheel --upload
