# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from flask import request

cred = credentials.Certificate('C:/Users/sahil/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def get_data():
    db = firestore.client()

    collection_ref = db.collection('lists')
    docs = collection_ref.get()
    json_obj = {}
    for doc in docs:
        doc_id = doc.id
        doc_data = doc.to_dict()
        json_obj[doc_id] = doc_data

    return jsonify(json_obj)

@app.route('/update', methods=['GET', 'POST'])
def update_interests():
    db = firestore.client()
    data = request.json.get('interests')
    db.collection('lists').document('dW8gYvJ1g88KdoqjSaws').update({'interests': firestore.ArrayUnion([data])})
    return 'ok'

@app.route('/update_key', methods=['GET', 'POST'])
def update_key_interests():
    db = firestore.client()
    data = request.json.get('interests')
    docs = db.collection('lists').where('interests', 'array_contains', 'bocce').get()
    for doc in docs:
        key = doc.id
        db.collection('lists').document(key).update({'interests': firestore.ArrayUnion([data])})
    return 'ok'


if __name__ == '__main__':
    app.run()