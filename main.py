from flask import jsonify, url_for

from app import create_app
from api import api

app = create_app()

@app.route('/')
def landing():
    return jsonify({'api': [url_for('api.hello', _external=True)]})

if __name__ == '__main__':
    app.register_blueprint(api)
    app.run(host='0.0.0.0', debug=True, port=8000)