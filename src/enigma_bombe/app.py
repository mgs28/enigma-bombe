"""
The main app for the enigma bombe which decodes a given cipher text
"""

import string

from flask import Flask, request

app = Flask(__name__)


@app.get("/ioc")
def index_of_coincidence():
    """
    Return the IC of a given piece of text, s, for an alphabet, a
    """
    s_in = request.args.get("s").lower()

    # convert to only characters
    s = ""
    for c in s_in:
        if c in string.ascii_lowercase:
            s += c

    h = {}
    for c in s:
        if c in h:
            h[c] = h[c] + 1
        else:
            h[c] = 1

    index_of_coincidence_metric = 0
    for k in h:
        index_of_coincidence_metric += h[k] * (h[k] - 1)

    n = len(s)
    index_of_coincidence_metric = index_of_coincidence_metric / (n * (n - 1))

    return f"{index_of_coincidence_metric}"
