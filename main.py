from scraper import get_albums
import random
import PySimpleGUI as sg
import webbrowser
from spotipy.oauth2 import SpotifyPKCE
import spotipy
import os
import pickle

def main():
    #authenticate spotify credentials
    auth_manager=SpotifyPKCE(client_id = '733feec74613475496335bd86b89e056',
        scope = 'user-top-read', redirect_uri='http://localhost:8888')
    cache_token = auth_manager.get_access_token()
    
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('ENTER A GENRE ("any" and "new" are valid entries)')],
                [sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Recommend something')] ]

    # Create the Window
    window = sg.Window('Choose albums', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        genre = ''
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == 'Recommend something':
            genre = get_user_top_genre(cache_token)
        if event == 'Ok':
            genre = values[0]
        make_window(genre, cache_token)        

    window.close()

def make_window(genre, cache_token):
    # get a list of albums
    albums = get_albums(genre, cache_token)
    albums_copy = albums[:]

    chosen_albums = []
    # take 9 random albums
    for x in range(1, 10):
        album = random.choice(albums_copy)
        albums_copy.remove(album)
        chosen_albums.append(album)
        # print(str(x) + '.', album, '\n')

    make_new_window(chosen_albums, albums)

def get_user_top_genre(cache_token):
    sp = spotipy.Spotify(cache_token)
    artists = sp.current_user_top_artists()['items']

    gFile = os.path.join("genreSet")
    infile = open(gFile,'rb')
    gSet = pickle.load(infile)
    infile.close()

    user_genres = set()

    for artist in artists:
        if 'genres' not in artist:
            continue
        g_list = artist['genres']
        for genre in g_list:
            user_genres.add(genre)

    chosen_genre = ''
    while chosen_genre.replace(' ', '-').lower() not in gSet and user_genres:
        chosen_genre = random.choice(tuple(user_genres))
        user_genres.remove(chosen_genre)

    if chosen_genre.replace(' ', '-').lower() not in gSet and not user_genres:
        return "any"

    return chosen_genre


def make_new_window(albums, full_list):
    grid = []

    for i in range(3):
        layout = []     
        for x in range(3):
            album = albums[i * 3 + x]
            layout.extend([sg.Image(data=album.get_png_data(), 
                enable_events=True, key=f"Link {i * 3 + x}")])

        grid.append(layout)

    grid.append([sg.Button('Ok'), sg.Button('More')])
    window = sg.Window("albums", grid)

    more = False
    chosen_albums = []
    while True:
        event, x = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok': # if user closes window or clicks cancel
            break
        if event.find('Link') == 0:
            album_num = int(event.split(' ')[1])
            curr_album = albums[album_num]
            webbrowser.open(curr_album.get_spotify_link())
        if event == 'More':
            chosen_albums = []
            albums_copy = full_list[:]
            for x in range(1, 10):
                album = random.choice(albums_copy)
                albums_copy.remove(album)
                chosen_albums.append(album)
            more = True
            break

    window.close()
    if more:
        make_new_window(chosen_albums, full_list)


if __name__ == '__main__':
    main()
