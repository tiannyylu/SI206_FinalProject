import unittest
import requests
import csv
import json
import sqlite3
import matplotlib.pyplot as plt
from textwrap import wrap
import spotify_info
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

clientID = spotify_info.SPOTIFY_CLIENT_ID
clientSecret = spotify_info.SPOTIFY_CLIENT_SECRET
redirectURI = spotify_info.SPOTIFY_REDIRECT_URI

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


#get albums data
def get_album(id):
    """ Uses an album id and the Spotify API to search for objects and
    parses through the results to create a new dictionary for each track

    id - spotify album id number
    """
    albumdict = {} # contains album name (key, value) and a list of track dictionaries under the key 'tracks'
    trackList = [] # a list of track dictionaries
    albumResults = sp.album(id)
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

def getSpotifyList(idLst):
    """ Creates a list of the album dictionaries with the keys, values from the get_album functions

    idList - a list of album IDs
    """
    spotifyList = []
    for id in idLst:
        results = get_album(id)
        spotifyList.append(results)
    return spotifyList

def addtoTable(spotifyList, conn, cur):
    """ Checks if there is a database called Albums and if not, then a new table is created
    with columns (album, artists_name, track, track_number, length_of_track). Then, the function
    iterates through the list of dictionaries and adds each element to the table.

    spotifyList - list of dictionaries for each album
    conn - connector
    cur - cursor to database
    """
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

def getTrackLengths(cur, spotifyList):
    """ Selects length of each track in the album and converts that time from milliseconds to minutes.
    Finds the average length of a song per album and adds the album name and average length
    to a dictionary and then writes the dictionary into a CSV file

    cur - cursor to database
    """
    avgDict= {}
    albumNames = [item['album_name'] for item in spotifyList]
    for name in albumNames:
        times = cur.execute('SELECT length_of_track FROM Albums where album = ?', (name,))
        minLst = []
        for t in times:
            seconds = (t[0]/1000.0)
            minutes = (seconds/60.0)
            minLst.append(minutes)
        avg = sum(minLst)/len(minLst)
        avg = round(avg, 2)
        avgDict[name] = avg
    myFile = open('avgLengths.csv', 'w')
    with myFile:
        headers = ['album names', 'average track length']
        writer = csv.DictWriter(myFile, fieldnames=headers)
        writer.writeheader()
        for item in avgDict.items():
            writer.writerow({'album names': item[0], 'average track length': item[1]})
    return avgDict

def drawBarChart(avgDict):
    """ Uses the dictionary of average length of a track for each albums and plots those values in a bar chart

    avgDict - a dictionary of album names as the keys and the average track length as the values
    """
    names = list(avgDict.keys())
    nums = list(avgDict.values())
    fig = plt.figure(figsize=(13,16))
    ax = fig.add_subplot(111)
    bars = ax.bar(names, nums)
    bars[0].set_color('lightsteelblue')
    bars[1].set_color('lightskyblue')
    bars[2].set_color('steelblue')
    bars[3].set_color('lightseagreen')
    bars[4].set_color('cadetblue')
    bars[5].set_color('lightslategray')
    bars[6].set_color('cornflowerblue')
    bars[7].set_color('midnightblue')
    ax.set_ylim(0,4.4)
    names = ['\n'.join(wrap(n, 20)) for n in names]
    ax.set_xticklabels(names,rotation=45,ha="right",rotation_mode='anchor')
    ax.set(xlabel='Album Names', ylabel='Average Song Length', title='Average Song Length of Popular Christmas Albums')
    fig.savefig('SongLengths.png')


# conn = sqlite3.connect('/Users/tiannyylu/Desktop/206_programs/final-project-tiannyylu/albums.sqlite')
# cur = conn.cursor()
#
# albumIDLst = ['3CKVXhODttZebJAzjUs2un','6zk4RKl6JFlgLCV4Z7DQ7N','61ulfFSmmxMhc2wCdmdMkN','5M8U1qYKvRQHJJVHmPY7QD','0ny6mZMBrYSO0s8HAKbcVq','3cr4Xgz8nnfp7iYbVqwzzH','6uIB97CqMcssTss9WrtX8c','7DuJYWu66RPdcekF5TuZ7w']
# spotifyList = getSpotifyList(albumIDLst)
#
# addtoTable(spotifyList, conn, cur)
#
# avgDict = getTrackLengths(cur)
# print(avgDict['Merry Christmas'])
# drawBarChart(avgDict)

class TestProject(unittest.TestCase):
    def setUp(self):
        clientID = spotify_info.SPOTIFY_CLIENT_ID
        clientSecret = spotify_info.SPOTIFY_CLIENT_SECRET
        redirectURI = spotify_info.SPOTIFY_REDIRECT_URI

        client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        self.conn = sqlite3.connect('/Users/tiannyylu/Desktop/206_programs/final-project-tiannyylu/albums.sqlite')
        self.cur = self.conn.cursor()

        albumIDLst = ['3CKVXhODttZebJAzjUs2un','6zk4RKl6JFlgLCV4Z7DQ7N','61ulfFSmmxMhc2wCdmdMkN','5M8U1qYKvRQHJJVHmPY7QD','0ny6mZMBrYSO0s8HAKbcVq','3cr4Xgz8nnfp7iYbVqwzzH','6uIB97CqMcssTss9WrtX8c','7DuJYWu66RPdcekF5TuZ7w']
        self.spotifyList = getSpotifyList(albumIDLst)
        addtoTable(self.spotifyList, self.conn, self.cur)

    def test_addtoTable(self):
        self.cur.execute('SELECT * FROM Albums')
        self.assertEqual(103, len(self.cur.fetchall()))

    def test_getTrackLengths(self):
        avgDict = getTrackLengths(self.cur, self.spotifyList)
        self.assertEqual(avgDict['Merry Christmas'], 3.8)

    def tearDown(self):
        self.conn.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)

TestProject().tearDown()
