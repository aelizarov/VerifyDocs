# VerifyDocs ID & NPI Checker

This is a python script/flask app to verify physicians using their passport, DOB, and NPI number.

# Setup

## Install Pipenv

```
$ pip install pipenv
```

```
$ pipenv --three
$ pipenv shell
$ pipenv install --skip-lock
```

## Run the Server

```
$ python main.py
```

Format: http://127.0.0.1:5000/?url={URL}&npi={NPI}&dob={DOB}&mode={MODE}

    URL - either a url to an image, a local uri, or byte-type
    NPI - a national provider identifier
    DOB (optional) - date of birth in the following format YYMMDD. Default None
    MODE - (int 1 or 0) whether the 'URL' is a url or something else

## Test CURL

```
curl --location --request GET 'http://127.0.0.1:5000/?url=https://answerdash-images.s3.amazonaws.com/1183/2163b3367a3c3d687ef68bba2b0b952c78f713e1/1528277944.perfect_20passport.jpg&npi=1427051077&dob=850117&mode=1'
```
