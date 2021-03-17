from datetime import datetime
from flask import request
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_file_content(file):
    f = open(file)
    content = f.read()
    return content


@app.route('/verify')
def check():
    token = request.headers['token']
    payload = {'foo': 'bar', 'wup': 90}

    pub_pem = str(get_file_content('public_pem')).encode('utf-8')
    pub_key = jwk.JWK.from_pem(pub_pem)
    try:
        headers, claims = jwt.verify_jwt(jwt=token, pub_key=pub_key, allowed_algs=['RS256'])
        print(headers)
        print(claims)
        result = True
        for k in payload:
            result = result and (claims[k] == payload[k])
        if result is True:
            return "success"
    except Exception as e:
        return "failed"


@app.route('/generate')
def hello():
    priv_pem = str(get_file_content('priv_pem')).encode('utf-8')
    payload = {'foo': 'bar', 'wup': 90}
    priv_key = jwk.JWK.from_pem(priv_pem)
    token = jwt.generate_jwt(claims=payload, priv_key=priv_key, algorithm='RS256',
                             lifetime=datetime.timedelta(minutes=5))
    return token

# @route('/code')
# def code():
#     # todo   produce the code
#     return "123456"

if __name__ == '__main__':
    app.run()
