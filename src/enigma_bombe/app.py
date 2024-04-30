"""
The main app for the enigma bombe which decodes a given cipher text
"""

from flask import Flask, request
from enigma_bombe.cipher_attack import CipherAttack

app = Flask(__name__)


@app.get("/ioc")
def index_of_coincidence():
    """
    Return the IC of a given piece of text, s
    """
    s = request.args.get("s")
    attack_vector = CipherAttack() 
    return f"{attack_vector.ioc_score(s)}"
