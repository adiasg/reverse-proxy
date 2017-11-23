from flask import Flask, render_template, request
import os
import socket
import hashlib

def hash(message):
    sha = hashlib.sha256()
    sha.update(message.encode('utf-8'))
    return sha.hexdigest()

def mine(message, difficulty):
    prefix = '0'*difficulty
    nonce = 0
    h = hash(message+str(nonce))
    while(not( ( h ).startswith(prefix) )):
        nonce += 1
        h = hash(message+str(nonce))
    return {'message': message, 'nonce': nonce, 'hash': h}

app = Flask(__name__)

@app.route("/")
def hello():
    # return str(request.headers)
    return render_template('index.html', hostname=socket.gethostname())

@app.route("/<int:difficulty>")
def test(difficulty):
    return str(mine("This is the message string.", difficulty))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
