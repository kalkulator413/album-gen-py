from scraper import get_albums
import random
import PySimpleGUI as sg
import requests
import textwrap

def main():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('ENTER A GENRE')],
                [sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('Choose albums', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

        # get genre from user
        genre = values[0]

        # get a list of albums
        albums = get_albums(genre)
        albums_copy = albums[:]

        chosen_albums = []
        # take 9 random albums
        for x in range(1, 10):
            album = random.choice(albums_copy)
            albums_copy.remove(album)
            chosen_albums.append(album)
            # print(str(x) + '.', album, '\n')

        make_new_window(chosen_albums, albums)

    window.close()

def make_new_window(albums, full_list):
    grid = []

    # length 9
    for i in range(3):

        # layout.append([sg.Text(album.name, font='Courier 12', text_color='white'), sg.Text(album.rating)])
        layout = []
        text = []
        artist = []
        genres = []
        size = (25, 2)
        for x in range(3):
            album = albums[i * 3 + x]
            s = wrap_str(album.name, int(1.3*size[0]))
            layout.extend([sg.Image(data=album.get_png_data())])
            text.extend([sg.Text(s, font='Courier 12', text_color='white', s=size), sg.Text(album.rating, font = "Courier 10")])

            artists = ''
            for a in album.artists:
                artists += a + ", "
            artists = artists[:-2]
            asize = (size[0] + 8, 2)
            a = wrap_str(artists, int(1.2*asize[0]))
            artist.extend([sg.Text(a, font="Courier 11", text_color='white', s=asize)])

        grid.append(layout)
        grid.append(text)
        grid.append(artist)

    grid.append([sg.Button('Ok'), sg.Button('More')])

    window = sg.Window("albums", grid)

    more = False
    chosen_albums = []
    while True:
        event, x = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok': # if user closes window or clicks cancel
            break
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

def wrap_str(n, size):
    album_name = textwrap.wrap(n, size)
    string = ''
    for s in album_name:
        string += s + '\n'
    return string


if __name__ == '__main__':
    main()