from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init database
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)


# Sentence Class/Model
class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String(350), unique=True)
    type_s = db.Column(db.String(50))

    def __init__(self, sentence, type_s):
        self.sentence = sentence
        self.type_s = type_s


# Sentence Schema
class SentenceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sentence', 'type_s')


# Init schema
sentence_schema = SentenceSchema()
sentences_schema = SentenceSchema(many=True)


# Create a sentence
@app.route('/sentence', methods=['POST'])
def add_sentence():
    sentence = request.json['sentence']
    type_s = request.json['type_s']

    new_sentence = Sentence(sentence, type_s)

    db.session.add(new_sentence)
    db.session.commit()

    return sentence_schema.jsonify(new_sentence)


# Get All Sentences
@app.route('/sentences', methods=['GET'])
def get_sentences():
    all_sentences = Sentence.query.all()
    result = sentences_schema.dump(all_sentences)
    return jsonify(result)


# Get Sentences By Id
@app.route('/sentence/<id>', methods=['GET'])
def get_certain_sentence_id(id):
    sentence = Sentence.query.get(id)
    return sentence_schema.jsonify(sentence)


# Update a sentence
@app.route('/sentence/<id>', methods=['PUT'])
def update_sentence(id):
    taken_sentence = Sentence.query.get(id)

    changed_sentence = request.json['sentence']
    changed_type_s = request.json['type_s']

    taken_sentence.sentence = changed_sentence
    taken_sentence.type_s = changed_type_s

    db.session.commit()

    return sentence_schema.jsonify(taken_sentence)


# Delete Sentence
@app.route('/sentence/<id>', methods=['DELETE'])
def delete_certain_sentence(id):
    sentence = Sentence.query.get(id)
    db.session.delete(sentence)
    db.session.commit()
    return sentence_schema.jsonify(sentence)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
