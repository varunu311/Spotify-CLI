import spotipy
import random
import sys  # Import sys to use sys.argv
from spotipy.oauth2 import SpotifyOAuth

# Your Spotify credentials and setup
client_id = "8052d2aea6234819887ed073fbd4837f"
client_secret = "3f5086a06cfa46a086ed52aa865bfcda"
redirect_uri = "http://localhost:3000/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-read-playback-state,user-modify-playback-state",
                                               cache_path="/path/to/your/cache/file"))  # Specify a full path for cache

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
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['uri']
        sp.start_playback(device_id=device_id, uris=[track_id])
    else:
        print("Song not found.")

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

def play_previous_track():
    sp.previous_track()

def play_next_track():
    sp.next_track()

def toggle_playback():
    current_playback = sp.current_playback()
    if current_playback is None or not current_playback['is_playing']:
        sp.start_playback()
    else:
        sp.pause_playback()

def add_song_to_queue(song_name):
    results = sp.search(q=song_name, limit=1)
    track_id = results['tracks']['items'][0]['uri']
    sp.add_to_queue(uri=track_id)

if __name__ == '__main__':
    # Check if a command-line argument (song name or command) was provided
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])  # Join all command-line arguments

        # Your existing command handling logic
        if command.startswith('-a'):
            artist_name = command[3:].strip()  # Ensure artist name is correctly extracted
            play_random_song_by_artist(artist_name)
        elif command.startswith('-l'):
            toggle_loop()
        elif command.startswith('-s'):
            toggle_shuffle()
        elif command.startswith('-prev'):
            play_previous_track()
        elif command.startswith('-next'):
            play_next_track()
        elif command.startswith('-pause') or command.startswith('-play'):
            toggle_playback()
        elif command.startswith('-q'):
            add_song_to_queue(command[3:])
        else:
            play_song(command)
    else:
        print("No command provided")