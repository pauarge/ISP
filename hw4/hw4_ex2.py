from flask import Flask, request
import bcrypt

app = Flask(__name__)


@app.route('/hw4/ex2', methods=['POST'])
def hello_world():
    request_json = request.get_json()
    password = request_json.get('pass')
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


app.run()
