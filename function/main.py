import requests
from datetime import datetime
from google.cloud import firestore

def save_to_firestore(song, station, collectionLog, collectionSongs):
    if check_songs(song, station, collectionLog):

        print(f"Saving the song: {song}")
    
        doc_ref = collectionSongs.document(song)
        doc_ref.set({
            u'name': song,
            u'station': station,
            u'date': str(datetime.now())
        })

def get_songs(radios):
    songs = []
    
    for radio in radios:
        try:
            r = requests.get('https://prod.radio-api.net/stations/' + radio + '/songs')
            r = r.json()
            songs.append([r[0]["rawInfo"].replace('/', ''), radio])
        except:
            continue

    return songs

def check_songs(song, station, collectionLog):
    docs = collectionLog.stream()

    print(f"Checking if the song was already saved: {song}")

    for doc in docs:
        if doc.to_dict()["name"] == song and doc.to_dict()["station"] == station:
            
            print(f"Song already saved: {song}")

            return False

    return True

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def add_to_logs(song, station, collectionLog):
    doc_ref = collectionLog.document(song)
    doc_ref.set({
        u'name': song,
        u'station': station
    })
    return

def hello_pubsub(event, context):
    db = firestore.Client()

    collectionSongs = db.collection('songs')
    collectionLog = db.collection('logs')

    infos = get_songs(['oe3', 'kronehit', 'radiowien', 'fm4'])

    for info in infos:
        save_to_firestore(info[0], info[1], collectionLog, collectionSongs)

    delete_collection(collectionLog, 50)

    for info in infos:
        add_to_logs(info[0], info[1], collectionLog)

    return
