import unittest
import requests
import json
import sqlite3
from datetime import date
import spotify_info
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

clientID = spotify_info.SPOTIFY_CLIENT_ID
clientSecret = spotify_info.SPOTIFY_CLIENT_SECRET
redirectURI = spotify_info.SPOTIFY_REDIRECT_URI

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


#get albums data
def get_album(albumIDLst):
    albumdict = {} # contains album name (key, value) and a list of track dictionaries under the key 'tracks'
    trackList = [] # a list of track dictionaries
    # trackdict = {} # a dictionary for a single track
    albumResults = sp.album(id)
    # for id in albumIDLst:
    albumName = albumResults['name']
    for track in albumResults['tracks']['items']:
        trackdict = {} # a dictionary for a single track
        trackdict['artist_name'] = track['artists'][0]['name']
        trackdict['track_name'] = track['name']
        trackdict['track_num'] = track['track_number']
        trackdict['track_lengthMS'] = track['duration_ms']
        trackList.append(trackdict)
    albumdict['album_name'] = albumName
    albumdict['tracks'] = trackList
    return albumdict


def addtoTable(spotifyList, conn, cur):
    cur.execute('CREATE TABLE IF NOT EXISTS Albums (album TEXT, artist_name TEXT, track TEXT, track_number INTEGER, length_of_track INTEGER)')
    for album in spotifyList:
        albumName = album['album_name']
        for track in album['tracks']:
            artist = track['artist_name']
            trackName = track['track_name']
            trackNum = track['track_num']
            trackLength = track['track_lengthMS']
            cur.execute('INSERT INTO Albums (album, artist_name, track, track_number, length_of_track) VALUES (?, ?, ?, ?, ?)', (albumName, artist, trackName, trackNum, trackLength))
    conn.commit()
    pass



albumIDLst = ['3CKVXhODttZebJAzjUs2un','6zk4RKl6JFlgLCV4Z7DQ7N','61ulfFSmmxMhc2wCdmdMkN','5M8U1qYKvRQHJJVHmPY7QD','0ny6mZMBrYSO0s8HAKbcVq','3cr4Xgz8nnfp7iYbVqwzzH','6uIB97CqMcssTss9WrtX8c','7DuJYWu66RPdcekF5TuZ7w']
spotifyList = []
for id in albumIDLst:
    results = get_album(id)
    spotifyList.append(results)
# print(spotifyList)
conn = sqlite3.connect('/Users/tiannyylu/Desktop/206_programs/final-project-tiannyylu/albums.sqlite')
cur = conn.cursor()

addtoTable(spotifyList, conn, cur)
