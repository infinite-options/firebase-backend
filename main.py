#!/usr/bin/env python
# coding: utf-8

# In[ ]:
#"GOOGLE_APPLICATION_CREDENTIALS" : "path/to/your/firebase/credentials.json"

from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import os


app = Flask(__name__)


cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

firebase_admin.initialize_app(cred)

@app.route('/data', methods=['GET'])
def get_data():
    db = firestore.client()

    collection_ref = db.collection('merch')
    docs = collection_ref.get()
    json_obj={}
    for doc in docs:
        doc_id = doc.id
        doc_data = doc.to_dict()
        json_obj[doc_id]=doc_data
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

@app.route('/updatefb', methods=['POST'])
def update():
    try:
        if request.is_json:
            db = firestore.client()
            req_data = request.get_json()

            collection = req_data['collection']
            document = req_data['document']
            field = req_data['field']
            new_value = req_data['new_value']

            doc_ref = db.collection(collection).document(document)

            doc = doc_ref.get()
            if doc.exists:
                if field in doc.to_dict():
                    doc_ref.update({field: firestore.ArrayUnion([new_value])})
                    return jsonify({"success": True, "message": "Value appended to field successfully."}), 200
                else:
                    return jsonify({"success": False, "message": "Field not found in the document."}), 404
            else:
                return jsonify({"success": False, "message": "Document not found in the collection."}), 404
        else:
            return jsonify({"success": False, "message": "Missing JSON in request body."}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)

