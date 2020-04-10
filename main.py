#!/usr/bin/env python
# coding: utf-8

from verifydocs import *
from flask import Flask, jsonify, request, wrappers

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root() -> wrappers.Response:
    url = request.args.get("url")
    npi = request.args.get("npi")
    dob = request.args.get("dob")
    mode = request.args.get("mode")
    if mode:
        url_mode = bool(int(mode))
    else:
        url_mode = True
    validity = validate(url, npi, dob, url_mode)
    return jsonify(validity)


if __name__ == "__main__":
    app.run()
