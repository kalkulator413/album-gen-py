from scraper import get_albums
import random

def main():
    # prompt user for a genre
    print("Enter a genre:")
    genre = input()

    # get a list of albums
    albums = get_albums(genre)

    # print received albums
    for x in range(1, 10):
        album = random.choice(albums)
        albums.remove(album)
        print(str(x) + '.', album, '\n')

if __name__ == '__main__':
    main()