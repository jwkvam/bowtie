.PHONY: test unit lint style eslint checkdocs coverage upload outdated

all: test

test:
	py.test --cov=./ --mypy --codestyle --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF

unit:
	py.test --cov=./

lint:
	py.test --pylint -m pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF

style:
	py.test --codestyle -m codestyle

eslint:
	eslint bowtie/src/*.js{,x}

checkdocs:
	pydocstyle --count --match-dir='(?!examples|build|doc|.*templates)[^\.].*'

coverage:
	py.test --cov=./ --cov-report html

loop:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF -f

debug:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF -s --pdb

static:
	mypy -p bowtie

monkeytype:
	monkeytype run `which pytest`

outdated:
	cd bowtie/src && yarn --ignore-engines install && yarn outdated
