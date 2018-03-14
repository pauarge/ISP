from flask import Flask, request, abort
import base64

app = Flask(__name__)

mySecureOneTimePad = "Never send a human to do a machine's job"


def superencryption(msg, key):
    if len(key) < len(msg):
        diff = len(msg) - len(key)
        key += key[0:diff]

    amsg = list(map(ord, list(msg)))
    akey = list(map(ord, list(key[0:len(msg)])))

    x = "".join(map(chr, [a ^ b for a, b in zip(amsg, akey)]))
    return base64.b64encode(x.encode('utf-8')).decode("utf-8")


@app.route('/hw2/ex1', methods=['POST'])
def hello_world():
    request_json = request.get_json()
    user = request_json.get('user')
    password = request_json.get('pass')
    if len(user) > 100 or len(password) > 100:
        return abort(400)

    enc = superencryption(user, mySecureOneTimePad)
    if password != enc:
        return abort(400)

    return 'Hello, World!'


app.run()
