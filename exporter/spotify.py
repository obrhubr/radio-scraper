import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import pandas as pd
import json

with open('exporter/spotify.json') as json_file:
    data = json.load(json_file)

client_id = data["client_id"]
client_secret = data["client_secret"]
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

def audio_features(track, idx):
    try:
        features = {'acousticness': 0, 'danceability': 0, 'energy': 0, 'instrumentalness': 0, 'liveness': 0, 'speechiness': 0, 'tempo': 0, 'valence': 0, 'loudness': 0, "index": 0}

        req = sp.audio_features(track)
        
        features['acousticness'] = req[0]['acousticness']
        features['danceability'] = req[0]['danceability']
        features['energy'] = req[0]['energy']
        features['instrumentalness'] = req[0]['instrumentalness']
        features['liveness'] = req[0]['liveness']
        features['loudness'] = req[0]['loudness']
        features['speechiness'] = req[0]['speechiness']
        features['tempo'] = req[0]['tempo']
        features['valence'] = req[0]['valence']

        features["index"] = idx
    except:
        return {}

    return features

if __name__ == "__main__":
    df = pd.read_csv('data/wrangled.csv', index_col=0)
    uri = []

    for idx, row in df.iterrows():
        print(idx, row["artist"], row["song"])
        searchResults = sp.search(q="track:" + row["song"], type="track")
        if len(searchResults["tracks"]["items"]) >= 1:
            uri.append(audio_features(searchResults["tracks"]["items"][0]["uri"], idx))

    df = df.join(pd.DataFrame(uri), lsuffix='_caller', rsuffix='_other')
    df = df.dropna()
    df.to_csv('data/spotify.csv')