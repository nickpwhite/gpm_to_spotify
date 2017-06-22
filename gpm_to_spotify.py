import json
import getpass
import os
import spotipy
import sys

from gmusicapi import Mobileclient

username = raw_input("Enter your Google Play Music email address: ")
password = getpass.getpass("Enter your password: ")

gpm_api = Mobileclient()
spotify = spotipy.Spotify()

if (not gpm_api.login(username, password, Mobileclient.FROM_MAC_ADDRESS, 'en_US')):
    print("Unable to login with the provided credentials.")
    sys.exit(-1)

out_file = open('out.txt', 'r+')
songs = gpm_api.get_all_songs()

# dump file for debugging
json.dump(songs, out_file, indent=4, sort_keys=True)

for track in songs[:1]:
    album = str(track[u'album'])
    artist = str(track[u'artist'])
    title = str(track[u'title'])
    print(album, artist, title)
    print(spotify.search(q=title, limit=20))
