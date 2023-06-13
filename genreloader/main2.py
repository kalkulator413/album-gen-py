import spotipy
import os
import pickle
from scraper import *
from spotipy.oauth2 import SpotifyPKCE
auth_manager=SpotifyPKCE(client_id = '733feec74613475496335bd86b89e056',
        scope = 'user-top-read', redirect_uri='http://localhost:8888')

cache_token = auth_manager.get_access_token()

num_pages = 3
genres = ['folk', 'rock', 'pop', 'hip-hop', 'electronic', 'jazz']

for genre in genres:
    albums = []
    base_url = 'https://rateyourmusic.com/charts/top/album/all-time/g:-rock,-pop,-folk,-hip-hop,-jazz,-electronic/'
    base_url = base_url.replace(f'-{genre}', genre)

    f = open(os.path.join("bruh", f"{genre}.txt"), "w")

    for pg in range(1, num_pages + 1):
        url = f'{base_url}/{pg}/'

        try:
            html = get_html(url)
        except Exception as e:
            print(e)
            raise Exception("unknown error")
        albums.extend(process_html(html, cache_token))

    for album in albums:
        if album.artists:
            f.write(f"['{album.artists[0]}', '{album.name}', '{genre}'], \n")
        else:
            print(album.name)
    f.close()