import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import numpy as np

def export_data_to_csv(collection):
    name, station, date = [], [], []
    docs = collection.stream()

    for doc in docs:
        data = doc.to_dict()
        name.append(data["name"])
        station.append(data["station"])
        date.append(data["date"])

    df = pd.DataFrame(np.column_stack([name, station, date]), columns=['name', 'station', 'date'])
    df.to_csv('data.csv')

if __name__ == "__main__":
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    songs = db.collection("songs")

    export_data_to_csv(songs)
    