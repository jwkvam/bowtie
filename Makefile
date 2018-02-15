.PHONY: test unit lint style eslint checkdocs coverage upload

all: test

test:
	py.test --cov=./ --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF --ignore=doc

test2:
	py.test --cov=./ --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF --ignore=doc --ignore=bowtie/_magic.py

unit:
	py.test --cov=./

lint:
	py.test --pylint -m pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF --ignore=doc

lint2:
	py.test --pylint -m pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF --ignore=doc --ignore=bowtie/_magic.py

style:
	py.test --codestyle -m codestyle --ignore=doc

eslint:
	eslint bowtie/src/*.js{,x}

checkdocs:
	pydocstyle --count --match-dir='(?!examples|build|doc|.*templates)[^\.].*'

coverage:
	py.test --cov=./ --cov-report html --ignore=doc

loop:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF -f --ignore=doc

debug:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF -s --pdb --ignore=doc
