import json
import getpass
import os
import re
import spotipy
import spotipy.util
import sys

from gmusicapi import Mobileclient

def gpm_login():
    gpm_api = Mobileclient()
    username = raw_input("Enter your Google Play Music email address: ")
    password = getpass.getpass("Enter your password: ")

    if (not gpm_api.login(username, password, Mobileclient.FROM_MAC_ADDRESS, 'en_US')):
        print("Unable to login to Google Play Music.")
        sys.exit(-1)

    return gpm_api

def spotify_login():
    scope = 'user-library-modify'
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    REDIRECT_URL = "http://localhost"

    spotify_username = raw_input("Enter your Spotify username: ")

    token = spotipy.util.prompt_for_user_token(spotify_username, scope, 
            SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URL)

    if (not token):
        print("Unable to get Spotify login token.")
        sys.exit(-1)

    return token

def sanitize(string):
    # new = re.sub('[!@#$%^&*=+_;:<>?|]', '', string)
    return re.sub('([Ff]t\.)|([Ff]eat\.)|([Ff]eaturing)', '', string)

def get_track_id(spotify, query):
    results = spotify.search(query, type='track')
    json.dump(results, result_file, indent=4, sort_keys=True)
    if (results['tracks']['total'] > 0):
        track_id = results['tracks']['items'][0]['id']
        for result in results['tracks']['items']:
            if (result['album']['name'] == album):
                track_id = result['id']

        return track_id
    else:
        return None

gpm_api = gpm_login()

token = spotify_login()

# Any existing output files with the same name will be overwritten when these are opened
out_file = open('out.txt', 'w')
result_file = open('results.txt', 'w')
not_added = open('not_added.txt', 'w')

print("Loading all songs from Google Play Music, this might take some time...")
songs = gpm_api.get_all_songs()

# dump file for debugging
json.dump(songs, out_file, indent=4, sort_keys=True)

spotify = spotipy.Spotify(auth=token)
ids = []

not_added.write("Couldn't add:\n")

for track in songs:
    album = track[u'album']
    artist = track[u'artist']
    title = track[u'title']

    queries = [u"track:{0} artist:{1}".format(sanitize(title), 
        sanitize(artist.replace('The ', '').replace("'", '')))]

    for item in artist.split('&'):
        queries.append(u"track:{0} artist:{1}".format(sanitize(title.split('(')[0]), 
            sanitize(item.replace('The ', '').replace("'", ''))))

    for query in queries:
        track_id = get_track_id(spotify, query)
        if (track_id is not None):
            break

    if (track_id is not None):
        ids.append(track_id)
    else:
        try:
            not_added.write(u"{0} - {1} - {2}\n".format(title, artist, album).encode('utf8'))
        except Exception as e:
            print(e)
            print(u"{0} - {1} - {2}\n".format(title, artist, album))

    if (len(ids) >= 50):
        print('Adding tracks (not really)')
        # spotify.current_user_saved_tracks_add(ids)
        ids = []
