from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])


@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'GET':
        return jsonify(message.to_dict())

    if request.method == 'PATCH':
        data = request.json
        if 'body' in data:
            message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())

    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return '', 204
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

if __name__ == '__main__':
    app.run(port=5555)
