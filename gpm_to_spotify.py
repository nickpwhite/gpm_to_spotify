import sys

def parse_link(gpm_link):
    raw_title = gpm_link.split('?t=')[1]
    song_info = raw_title.split('-')
    title = song_info[0].replace('_', ' ').strip()
    artist = song_info[1].replace('_', ' ').strip()
    return title, artist 

if (len(sys.argv) > 1):
    for arg in sys.argv[1:]:
        print(parse_link(arg))
else:
    print("no args provided");
