#Getting Started

##If you don't have pipenv

```
$ pip install pipenv
```

##Setup

```
$ pipenv
$ pipenv shell
$ pipenv install --skip-lock
```

##To run the demo flask server

```
$ python main.py
```

Format: http://127.0.0.1:5000/?url={URL}&npi={NPI}&dob={DOB}&mode={MODE}

	URL - either a url to an image, a local uri, or byte-type.
	NPI - a national provider identifier.
	DOB (optional) - date of birth in the following format YYMMDD. Default None.
	MODE - whether the 'URL' is a url or something else. Default True.

##To use the package




