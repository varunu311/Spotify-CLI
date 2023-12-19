import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth

client_id = "8052d2aea6234819887ed073fbd4837f"
client_secret = "3f5086a06cfa46a086ed52aa865bfcda"
redirect_uri = "http://localhost:3000/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-read-playback-state,user-modify-playback-state"))
def get_active_device():
    devices = sp.devices()
    for device in devices['devices']:
        if device['is_active']:
            return device['id']
    return None

def play_song(song_name):
    device_id = get_active_device()
    if device_id is None:
        print("No active device found. Please open Spotify on your device.")
        return
    results = sp.search(q=song_name, limit=1)
    track_id = results['tracks']['items'][0]['uri']
    sp.start_playback(device_id=device_id, uris=[track_id])

def play_random_song_by_artist(artist_name):
    results = sp.search(q=artist_name, limit=50, type='artist')
    artist_id = results['artists']['items'][0]['id']
    tracks = sp.artist_top_tracks(artist_id)['tracks']
    random_track_uri = random.choice(tracks)['uri']
    sp.start_playback(uris=[random_track_uri])

def toggle_loop():
    current_playback = sp.current_playback()
    if not current_playback or not current_playback['is_playing']:
        print("No active playback found.")
        return
    sp.repeat('track' if current_playback['repeat_state'] != 'track' else 'off')

def toggle_shuffle():
    current_playback = sp.current_playback()
    if not current_playback:
        print("No active playback found.")
        return
    sp.shuffle(not current_playback['shuffle_state'])

if __name__ == '__main__':
    command = input("Enter your command: ")

    if command[:2] == '-a':
        play_random_song_by_artist(command[3:])
    elif command[:2] == '-l':
        toggle_loop()
    elif command[:2] == '-s':
        toggle_shuffle()
    else:
        play_song(command)