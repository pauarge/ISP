from flask import Flask, request, abort
import datetime
import time
import base64
import hmac

key = "PgQDSxNSFAACBUcURRw1CBEITFoMSA==".encode('utf-8')
app = Flask(__name__)


def generate_cookie(user, admin=False):
    dts = datetime.datetime.utcnow()
    epochtime = round(time.mktime(dts.timetuple()) + dts.microsecond / 1e6)
    perm = "administrator" if admin else "user"
    hm = hmac.new(key, "{}{}".format(user, epochtime).encode('utf-8'))
    s = "{},{},com402,hw2,ex3,{},{}".format(user, epochtime, perm, hm.digest())
    return base64.b64encode(s.encode('utf-8'))


@app.route('/ex3/login', methods=['POST'])
def ex3login():
    request_json = request.get_json()
    user = request_json.get('user')
    password = request_json.get('pass')

    response = app.make_response("Login page")
    if user and password:
        response.set_cookie('cookie_name', value='values')

        if user == "administrator" and password == "42":
            response.set_cookie('LoginCookie', value=generate_cookie(user, True))
        else:
            response.set_cookie('LoginCookie', value=generate_cookie(user, False))

    return response


@app.route('/ex3/list', methods=['POST'])
def ex3list():
    if 'LoginCookie' in request.cookies:
        loginCookie = base64.b64decode(request.cookies.get('LoginCookie'))
        fields = loginCookie.split(',')
        return "Cool."
    else:
        return abort(403)


app.run()
