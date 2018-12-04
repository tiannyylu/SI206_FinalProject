import unittest
import requests
import json
from datetime import date
import spotify_info
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

clientID = spotify_info.SPOTIFY_CLIENT_ID
clientSecret = spotify_info.SPOTIFY_CLIENT_SECRET
redirectURI = spotify_info.SPOTIFY_REDIRECT_URI

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


fname = 'cacheSpotifyData.json'
try:
    cache_file = open(fname, 'r')
    cache_contents = cache_file.read()
    cacheDict= json.loads(cache_contents)
    cache_file.close()
except:
    cacheDict = {}

#get albums data
def get_album(id):
    today = str(date.today())
    k = id + '(' + today +')' #album ID and the current date
    if k in cacheDict:
        print('data is already in cache')
        return cacheDict[k]
    else:
        print('fetching data')
        albumResults = sp.album(id)
        try:
            cacheDict[k] = albumResults
            dumped_json_cache = json.dumps(cacheDict)
            file_write = open(fname,"w")
            file_write.write(dumped_json_cache)
            file_write.close() # Close the open file
            return cacheDict[k]
        except:
            print("Wasn't in cache and wasn't valid search either")
            return None

def addToTable(spotifyList, conn, cur):
    pass



albumIDLst = ['3CKVXhODttZebJAzjUs2un','6zk4RKl6JFlgLCV4Z7DQ7N','61ulfFSmmxMhc2wCdmdMkN','5M8U1qYKvRQHJJVHmPY7QD','0ny6mZMBrYSO0s8HAKbcVq','3cr4Xgz8nnfp7iYbVqwzzH','6uIB97CqMcssTss9WrtX8c']
for id in albumIDLst:
    result = get_album(id)
    print(result['popularity'])
    print(result['release_date'])
