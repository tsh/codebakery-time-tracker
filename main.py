from flask import Flask, jsonify

from app import create_app

app = create_app()

@app.route('/')
def hello_world():
    return jsonify({'hello': 'world'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)