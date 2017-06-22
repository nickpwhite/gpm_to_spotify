import json
import getpass
import os
import sys

from gmusicapi import Mobileclient

def parse_link(gpm_link):
    raw_title = gpm_link.split('?t=')[1]
    song_info = raw_title.split('-')
    title = song_info[0].replace('_', ' ').strip()
    artist = song_info[1].replace('_', ' ').strip()
    return title, artist 

username = raw_input("Enter your Google Play Music email address: ")
password = getpass.getpass("Enter your password: ")

gpm_api = Mobileclient()

if(not gpm_api.login(username, password, Mobileclient.FROM_MAC_ADDRESS, 'en_US')):
    print("Unable to login with the provided credentials.")
    sys.exit(-1)

out_file = open('out.txt', 'w')
songs = gpm_api.get_all_songs()

json.dump(songs, out_file, indent=4, sort_keys=True)

# if (len(sys.argv) > 1):
    # for arg in sys.argv[1:]:
        # print(parse_link(arg))
# else:
    # while True:
        # try:
            # gpm_link = raw_input("Enter a Google Play Music link (^D to exit): ")
            # print(parse_link(gpm_link))
        # except EOFError:
            # break
