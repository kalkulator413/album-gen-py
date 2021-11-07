# from command import *
from bs4 import BeautifulSoup as soup
import random
import requests
import urllib.request
import re

OS = ('Windows NT 10.0; Win64; x64', 'Windows NT 5.1', 'Windows NT 6.1; Win64; x64', 'Windows NT 6.1; WOW64', 'Windows NT 10.0; WOW64', 'Windows NT 10.0', 'X11; Linux x86_64')
WEBKIT = ('537.1', '537.36', '605.1.15')
CHROME = ('21.0.1180.83', '44.0.2403.157', '46.0.2490.71', '56.0.2924.76', '60.0.3112.90', '60.0.3112.113', '63.0.3239.132', '65.0.3325.181', '67.0.3396.99', '68.0.3440.106', '69.0.3497.100', '72.0.3626.121', '74.0.3729.131', '74.0.3729.157', '74.0.3729.169', '78.0.3904.108', '79.0.3945.88', '79.0.3945.117', '79.0.3945.130', '80.0.3987.132', '80.0.3987.163', '81.0.4044.138', '83.0.4103.116', '84.0.4147.105', '84.0.4147.135', '85.0.4183.83', '85.0.4183.102', '85.0.4183.121', '86.0.4240.16', '86.0.4240.111', '87.0.4280.40', '88.0.4298.4', '88.0.4324.146', '88.0.4324.150')
SAFARI = ('537.1', '537.36', '604.1')

year = '2021'
genreTypes = ["Any", "New", "Hip Hop", "Pop", "Rock", "Folk", "Shoegaze", "Dream Pop", "Experimental", "Punk", "Blues", "Jazz", "Screamo"];

class Album:
	def __init__(self, name, artists, rating, genres, link):
		self.name = clean_name(name)
		self.artists = artists
		self.rating = get_rating(rating)
		self.genres = genres
		self.link = link if link[0] != '/' else 'https:' + link

	def __str__(self):
		artists = ''
		for artist in self.artists:
			artists += artist + ", "
		artists = artists[:-2]

		genres = ''
		for genre in self.genres:
			genres += genre + ", "
		genres = genres[:-2]

		return self.name + "\n" + artists + "\n" + self.link[8:] + "\n" + genres + '\n' + self.rating

def get_rating(rating):
	res = int(100*(2 * float(rating) + 1.50))/100.
	return str(res) if res <= 10 else '10.0'

def clean_name(name):
	if name and name[0] in [' ', '\n', '\t']:
		return clean_name(name[1:])
	return clean_helper(name).replace("amp;", "")

def clean_helper(name):
	if name and name[-1] in  [' ', '\n', '\t']:
		return clean_helper(name[:-1])
	return name

def get_num_pages(genre):
	if genre in ['Any', 'any']:
		return 6
	elif genre in ['New', 'new']:
		return 3
	return 4

def get_url(genre):
	if genre in ['New', 'new']:
		return "https://rateyourmusic.com/charts/top/album,mixtape/" + year + "/"
	return "https://rateyourmusic.com/charts/top/album,mixtape/all-time/g:" + genre.lower().replace(' ', '-') + '/'

def get_html(url):
	# proxy = urllib.request.ProxyHandler(proxies=proxyDict)
	# opener = urllib.request.build_opener(proxy)
	# urllib.request.install_opener(opener)

	req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(OS) + ') AppleWebKit/' + random.choice(WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(CHROME) + ' Safari/' + random.choice(SAFARI)})
	return soup(urllib.request.urlopen(req).read(), 'html.parser').prettify()

def parse_element(init, final, data):
	start = data.find(init) + len(init)
	end = data[start:].find(final) + start
	return data[start:end], end

def get_albums(html):
	while html.find('href="/release/album/') >= 0:

		album_data, end_index = parse_element('href="/release/album/', '<div class="topcharts_item_medialinkbox">', html)

		image, x = parse_element('src="', '"', album_data)

		album_data = album_data[album_data.find('title="[Album') + len('title="[Album'):]
		name, x = parse_element('>', '<', album_data)

		artists = []
		while album_data.find('class="artist') >= 0:
			album_data = album_data[album_data.find('class="artist"') + len('class="artist"'):]
			artist, x = parse_element('>', '<', album_data)
			artists.append(clean_name(artist))

		rating, x = parse_element('topcharts_avg_rating_stat">', '<', album_data)

		genres = []
		while album_data.find('class="genre topcharts_item_genres"') >= 0:
			album_data = album_data[album_data.find('class="genre topcharts_item_genres"') + len('class="genre topcharts_item_genres"'):]
			genre, x = parse_element('>', '<', album_data)
			genres.append(clean_name(genre))

		# hardcoded:
		if '★' in name:
			name = 'Blackstar'

		albums.append(Album(name, artists, clean_name(rating), genres, image))

		html = html[end_index:]

genre = 'New'#lookup[1]


albums = []

for x in range(1, get_num_pages(genre) + 1):
	if x == 1:
		url = get_url(genre)
	else:
		url = get_url(genre) + str(x) + "/#results"

	html = get_html(url)
	get_albums(html)

for x in range(1, 10):
	album = random.choice(albums)
	albums.remove(album)

	print(str(x) + '.', album, '\n')
