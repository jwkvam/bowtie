# bowtie

## Install

To do a local install you need python 3 to create a python wheel package with flit.

```
flit wheel
```

You can then pip install the wheel locally, e.g.

```
pip install dist/bowtie-0.0.1_dev-py2.py3-none-any.whl
```
Then do
```
pip install -r requirements.txt
```
Once I hit an MVP I'll upload it to pypi and this will be much easier...

## Requirements

Install [node](https://nodejs.org/en/) and install `webpack` globally.

```
npm install -g webpack
```

## Example

See `example.py` for an example app.
Run `python example.py` to build the app then run `./build/src/server.py` to launch the webapp.
