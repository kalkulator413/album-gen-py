from email.utils import localtime
from urllib.request import Request, urlopen
import random
from Album import Album
import pickle
import os
import time

_OS = ('Windows NT 10.0; Win64; x64', 'Windows NT 5.1', 'Windows NT 6.1; Win64; x64', 'Windows NT 6.1; WOW64', 'Windows NT 10.0; WOW64', 'Windows NT 10.0', 'X11; Linux x86_64')
_WEBKIT = ('537.1', '537.36', '605.1.15')
_CHROME = ('21.0.1180.83', '44.0.2403.157', '46.0.2490.71', '56.0.2924.76', '60.0.3112.90', '60.0.3112.113', '63.0.3239.132', '65.0.3325.181', '67.0.3396.99', '68.0.3440.106', '69.0.3497.100', '72.0.3626.121', '74.0.3729.131', '74.0.3729.157', '74.0.3729.169', '78.0.3904.108', '79.0.3945.88', '79.0.3945.117', '79.0.3945.130', '80.0.3987.132', '80.0.3987.163', '81.0.4044.138', '83.0.4103.116', '84.0.4147.105', '84.0.4147.135', '85.0.4183.83', '85.0.4183.102', '85.0.4183.121', '86.0.4240.16', '86.0.4240.111', '87.0.4280.40', '88.0.4298.4', '88.0.4324.146', '88.0.4324.150')
_SAFARI = ('537.1', '537.36', '604.1')
_year = '2022'

def get_albums(genre):

    f = os.path.join('data', genre.replace(" ", "-").lower())
    time_diff = 0

    if os.path.exists(f):
        filemade = time.localtime(os.path.getctime(f))
        filemade = int(time.strftime('%j', filemade))
        current_time = time.localtime()
        current_time = int(time.strftime('%j', current_time))
        time_diff = abs(current_time - filemade)
        
    
    if os.path.exists(f) and time_diff < 7:
        infile = open(f,'rb')
        albums = pickle.load(infile)
        infile.close()
    else:
        albums = []
        num_pages = get_num_pages(genre)

        gFile = os.path.join("genreSet")
        infile = open(gFile,'rb')
        gSet = pickle.load(infile)
        infile.close()

        if genre.replace(" ", "-").lower() not in gSet:
            raise Exception("Invalid genre. Valid genres include new, any, pop, rock, folk, hip-hop, and others")

        for pg in range(1, num_pages + 1):
            url = get_url(genre, pg)
            try:
                html = get_html(url)
            except Exception as e:
                print(e)
                raise Exception("unknown error")
            albums.extend(process_html(html))

        outfile = open(f,'wb')
        pickle.dump(albums, outfile)
        outfile.close()

    return albums

def get_num_pages(genre):
	if genre.lower() == 'any':
		return 6
	elif genre.lower() == 'new':
		return 3
	return 4

def get_url(genre, pg):
    if genre.lower() == 'new':
        url = "https://rateyourmusic.com/charts/top/album,mixtape/" + _year + "/"
    elif genre.lower() == 'any':
        url = "https://rateyourmusic.com/charts/top/album,mixtape/all-time/"
    else:
        url = "https://rateyourmusic.com/charts/top/album,mixtape/all-time/g:" + genre.lower().replace(' ', '-') + '/'
    
    if pg == 1:
        return url
    return url + str(pg) + "/#results"

def get_html(url):
	req = Request(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(_OS) + 
        ') AppleWebKit/' + random.choice(_WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(_CHROME) + 
        ' Safari/' + random.choice(_SAFARI)})
	return urlopen(req).read().decode('utf-8')

def process_html(html):
    albums = []

    while html.find('<div id="pos') >= 0:
        album_data, end_index = parse_element('<div id="pos', 'class="media_link_container lazyload">', html)
        
        _, x = parse_element('type="image/webp"', '//', album_data)
        image, y = parse_element('//', '.webp', album_data[x:])
 
        name, x = parse_element('<span class="ui_name_locale_original">', '<', album_data)
        album_data = album_data[x:]

        artists = []
        while album_data.find('<span class="ui_name_locale_original">') >= 0:
            album_data = album_data[album_data.find('<span class="ui_name_locale_original">') + len('<span class="ui_name_locale_original"'):]
            artist, x = parse_element('>', '<', album_data)
            artists.append(clean_name(artist))

        while album_data.find('<span class="ui_name_locale"') >= 0:
            album_data = album_data[album_data.find('<span class="ui_name_locale"') + len('<span class="ui_name_locale"'):]
            artist, x = parse_element('>', '<', album_data)
            artists.append(clean_name(artist))

        rating, x = parse_element('<span class="page_charts_section_charts_item_details_average_num">', '<', album_data)

        genres = []
        while album_data.find('<a class="genre comma_separated"') >= 0:
            album_data = album_data[album_data.find('<a class="genre comma_separated"') + len('<a class="genre comma_separated"'):]
            genre, x = parse_element('>', '<', album_data)
            genres.append(genre)

        # hardcoded:
        if '★' in name:
            name = 'Blackstar'

        albums.append(Album(clean_name(name), artists, rating, genres, image))

        html = html[end_index:]
    return albums

def parse_element(init, final, data):
	start = data.find(init) + len(init)
	end = data[start:].find(final) + start
	return data[start:end], end

def clean_name(name):
    return name.replace("&#39;", "'").replace("&amp;", "&").replace("&quot;", "\"")