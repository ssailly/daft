import json
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

props_file = 'props.json'

with open(props_file) as f: props = json.load(f)

scope = 'playlist-read-private,playlist-read-collaborative,' + \
        'playlist-modify-public,playlist-modify-private,user-library-read'

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id = props['client_id'],
        client_secret = props['client_secret'],
        redirect_uri = props['redirect_uri'],
        scope = scope
    )
)

current_user_id = sp.me()['id']

offset = 0
saved_tracks_ids, last_saved_tracks = [], []
saved_tracks_window = sp.current_user_saved_tracks(limit = 50, offset = offset)
while len(saved_tracks_window['items']) > 0:
    if offset == 0: last_saved_tracks = saved_tracks_window
    saved_tracks_ids += [
        item['track']['id'] for item in saved_tracks_window['items']
    ]
    offset += 50
    saved_tracks_window = sp.current_user_saved_tracks(
        limit = 50,
        offset = offset
    )

playlists = sp.current_user_playlists(limit = 50)
last_50_id, last_50_name = '', props['last_50_name']
rand_50_id, rand_50_name = '', props['rand_50_name']
for playlist in playlists['items']:
    if playlist['owner']['id'] == current_user_id:
        if playlist['name'] == last_50_name: last_50_id = playlist['id']
        elif playlist['name'] == rand_50_name: rand_50_id = playlist['id']

if last_50_id == '': 
    last_50_id = sp.user_playlist_create(current_user_id, last_50_name)['id']
sp.playlist_replace_items(last_50_id, [])
for item in last_saved_tracks['items']:
    track = item['track']
    sp.playlist_add_items(last_50_id, [track['id']])

if rand_50_id == '':
    rand_50_id = sp.user_playlist_create(current_user_id, rand_50_name)['id']
sp.playlist_replace_items(rand_50_id, [])
random.shuffle(saved_tracks_ids)
for track_id in saved_tracks_ids[:50]:
    sp.playlist_add_items(rand_50_id, [track_id])
