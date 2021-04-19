import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import numpy as np

def stream_collection_loop(collection, cursor=None):
    limit = 100
    while True:
        docs = []  # Very important. This frees the memory incurred in the recursion algorithm.
        if cursor:
            docs = [snapshot for snapshot in
                    collection.limit(limit).start_after(cursor).stream()]
        else:
            docs = [snapshot for snapshot in collection.limit(limit).stream()]

        export_data_to_csv(docs)

        if len(docs) == limit:
            cursor = docs[limit-1]
            continue

        break

def export_data_to_csv(docs):
    name, station, date = [], [], []

    for doc in docs:
        data = doc.to_dict()
        name.append(data["name"])
        station.append(data["station"])
        date.append(data["date"])

    df = pd.DataFrame(np.column_stack([name, station, date]), columns=['name', 'station', 'date'])
    with open('data/data.csv', 'a') as f:
        df.to_csv('data/data.csv', mode='a', header=f.tell()==0, index=False)

if __name__ == "__main__":
    cred = credentials.Certificate('exporter/key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    songs = db.collection("songs")

    stream_collection_loop(songs)
    