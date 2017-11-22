from flask import Flask, render_template, request
import os
import socket

app = Flask(__name__)

@app.route("/")
def hello():
    # return str(request.headers)
    return render_template('index.html', hostname=socket.gethostname())

@app.route("/<int:x>")
def fact(x):
    if x<0:
        return "Invalid number"
    fact = 1
    for i in range(1,x+1):
        fact = fact*i
    return str(fact)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
