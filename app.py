import flask

from util.authentication import Authentication

app = flask.Flask(__name__)


@app.route("/create_user", methods=["GET"])
def authenticate():
    if not flask.request.json['username'] or flask.request.json['passwd']:
        flask.abort(400)

    username = flask.request.json['username']
    passwd = flask.request.json['passwd']

    authentication_object = Authentication(username, passwd)
    if authentication_object.authenticate()[0]:
        return flask.make_response(flask.jsonify({'status':'success'}), 200)
    else:
        return flask.make_response(flask.jsonify({'error': 'success'}), 500)



'''
THIS FILE NEEDS MORE WORK
'''