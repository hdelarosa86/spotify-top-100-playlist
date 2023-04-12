import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
ENDPOINT = 'https://www.billboard.com/charts/hot-100/'
REDIRECT_URI = 'http://example.com'

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
))

date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')
year = date[:4]
response = requests.get(f'{ENDPOINT}{date}/')
web_page_data = response.text

soup = BeautifulSoup(web_page_data, 'html.parser')

music_list = soup.select(selector='.o-chart-results-list__item h3')
top_100_songs = [song.getText().strip() for song in music_list]

tracks_uris = []
for song in top_100_songs:
    query = sp.search(q=f"track:{song} year:{year}")
    try:
        song_uri = query['tracks']['items'][0]['uri']
    except IndexError:
        print('No song found')
    else:
        tracks_uris.append(query['tracks']['items'][0]['uri'])

user_id = sp.current_user()['id']

playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)['id']
sp.playlist_add_items(playlist_id=playlist_id, items=tracks_uris)
