import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = "playlist-modify-private"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
top_100 = []

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                    client_id=client_id,
                                                    client_secret=client_secret,
                                                    redirect_uri="http://example.com",
                                                    ))

user_id = spotify.current_user()["id"]

for title in soup.select(".o-chart-results-list__item h3"):
    titles = title.getText().strip()
    top_100.append(titles)

year = date.split("-")[0]
song_uris = []

for song in top_100:
    results = spotify.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = spotify.user_playlist_create(user=user_id, name=f"{date} Billbaord 100", public=False)
spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)