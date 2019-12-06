#!/usr/bin/env python
import os
import sys
import requests
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
import torch

cred = credentials.Certificate("Firebase/waste-sorting-e9400-252b22c7607d.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'waste-sorting-e9400.appspot.com'
})
bucket = storage.bucket()
db = firestore.client()

def updateRecent(predictions, name, time):
    first_class = predictions[5][0]
    second_class = predictions[4][0]
    third_class = predictions[3][0]
    first_confidence = round(torch.IntTensor.item(predictions[5][1]) * 100, 2)
    second_confidence = round(torch.IntTensor.item(predictions[4][1]) * 100, 2)
    third_confidence = round(torch.IntTensor.item(predictions[3][1]) * 100, 2)
    data = {
        u'firstClass': first_class,
        u'secondClass': second_class,
        u'thirdClass': third_class,
        u'firstConfidence': first_confidence,
        u'secondConfidence': second_confidence,
        u'thirdConfidence': third_confidence,

        u'name': u'' + name,
        u'timestamp': time
    }
    db.collection('Live').document("recent").set(data)

def uploadToFirebase(filename, typeOfTrash, predictions):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H.%M.%S")

    doc_ref = db.collection("Bin3").document()
    id = doc_ref.id
    print(id)
    data = {
        u'timestamp': now,
        u'location': u'uni',
        u'name': u''+id,
        u'type': u''+typeOfTrash,
        u'validations': {
            u'cardboard': 0,
            u'glass': 0,
            u'metal': 0,
            u'paper': 0,
            u'plastic': 0,
            u'trash': 0,
        }
    }
    db.collection('Bin3').document(id).set(data)
    blob = bucket.blob(id + ".jpg")
    blob.upload_from_filename(filename)

    updateRecent(predictions, id, now)

    print(blob.public_url)