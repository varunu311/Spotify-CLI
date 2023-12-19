import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "8052d2aea6234819887ed073fbd4837f"
client_secret = "3f5086a06cfa46a086ed52aa865bfcda"
redirect_uri = "http://localhost:3000/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-read-playback-state,user-modify-playback-state"))

song_name = input("Enter the name of the song you want to play: ")
results = sp.search(q=song_name, limit=1)
track_id = results['tracks']['items'][0]['uri']
sp.start_playback(uris=[track_id])
