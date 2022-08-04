from scraper import get_albums
import random
import PySimpleGUI as sg
import webbrowser
from Album import authenticate

def main():
    #authenticate spotify credentials
    authenticate()
    
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('ENTER A GENRE ("any" and "new" are valid entries)')],
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
