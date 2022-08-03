import os
import pickle

genres = set()

f = os.path.join("genres")
with open(f) as file:
    while True:
        line = file.readline()
        if not line: 
            break
        genres.add(line[:-1].replace(' ', '-').lower())

f = os.path.join("genreSet")
with open(f, 'wb') as file:
    pickle.dump(genres, file)