from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cloudscraper
import io
import os
IMAGE_WIDTH = 200
import spotipy

class Album:

	def __init__(self, name, artists, rating, genres, link, cache_token):
		self.name = name
		self.artists = artists
		self.rating = Album._get_rating(rating)
		self.genres = genres
		self.link = 'https://' + link
		self.sp = spotipy.Spotify(cache_token)

	def __str__(self):
		return self.name + "\n" + self.get_artists_as_str() + "\n" + self.link + "\n" + self.get_genres_as_str() + '\n' + self.rating

	def get_spotify_link(self):
		try:
			results = self.sp.search(q = 'artist:' + self.artists[0] + ' album:' + self.name, type = 'album')
			items = results['albums']['items']
			if len(items) > 0:
				album = items[0]
				return 'https://open.spotify.com/album/' + album['id']
			return 'https://open.spotify.com/search/' + self.name.lower().replace(' ', '%20') + '%20' + self.artists[0].lower().replace(' ', '%20')
		except Exception as e:
			print(e)
			print("Couldnt find link for album")
			return ("https://open.spotify.com/")

	def get_artists_as_str(self):
		artists = ''
		for artist in self.artists:
			artists += artist + ", "
		return artists[:-2]

	def get_genres_as_str(self):
		g = ''
		for genre in self.genres:
			g += genre + ", "
		return g[:-2]

	def get_album_img(self):
		try:
			results = self.sp.search(q="artist:" + self.artists[0] + " album:" + self.name, type="album")
			items = results['albums']['items']
			album = items[0]
			return album['images'][0]['url']
		except:
			return ('https://e.snmc.io/i/600/s/8559a4fc4072bf4049920706e223a5af/8703155/' 
					+ 'critarc-x-jumbudrif-this-image-is-blocked-either-due-to-legal-restri'
					+ 'ctions-in-your-country-or-due-to-your-personal-settings-login-and-go-to-your-account-options-to-see-more-info-Cover-Art.jpg')

	def get_png_data(self):
		if self.link.rstrip() != 'https://':
			url = self.link
		else:
			url = self.get_album_img()
		jpg_data = (
			cloudscraper.create_scraper(
				browser={"browser": "firefox", "platform": "windows", "mobile": False}
			)
			.get(url)
			.content
		)

		pil_image = Image.open(io.BytesIO(jpg_data))

		wpercent = (IMAGE_WIDTH/float(pil_image.size[0]))
		hsize = int((float(pil_image.size[1])*float(wpercent)))
		pil_image = pil_image.resize((IMAGE_WIDTH,hsize), Image.ANTIALIAS)
		w, h = pil_image.size

		extra_height = int(round(IMAGE_WIDTH/3))
		background = Image.new('RGBA', (IMAGE_WIDTH, extra_height), (0, 0, 0, 0))
		I1 = ImageDraw.Draw(background)

		fontSize = int(round(IMAGE_WIDTH / 12))
		if (len(self.name) > 20):
			fontSize = int(round(IMAGE_WIDTH * 20 / 12 / len(self.name)))
		ttf = ImageFont.truetype(os.path.join("Arial-Unicode-Bold.ttf"), fontSize)
		I1.text((0, 0), self.name, (255, 255, 255), font=ttf)

		fontSize = int(round(IMAGE_WIDTH / 14))
		if (len(self.get_artists_as_str()) > 23):
			fontSize = int(round(IMAGE_WIDTH * 23 / 14 / len(self.get_artists_as_str())))
		ttf = ImageFont.truetype(os.path.join("Arial-Unicode-Bold.ttf"), fontSize)
		I1.text((0, int(round(extra_height * .25))), self.get_artists_as_str(), (200, 200, 200), font = ttf)

		r = float(self.rating)
		red = 550 - int(55 * r)
		if (red > 255):
			red = 255
		
		green = -295 + int(55 * r)
		if (green < 0):
			green = 0

		ratio = 255.0 / green
		red = int(ratio * red)
		if (red > 255):
			red = 255

		fontSize = int(round(IMAGE_WIDTH / 15))
		ttf = ImageFont.truetype(os.path.join("Arial-Unicode-Bold.ttf"), fontSize)
		I1.text((0, int(round(.5*extra_height))), self.rating, (red, 255, 0), font=ttf)

		gcopy = self.genres[:]
		gtext = Album._list_to_str(gcopy)
		while (len(gtext) > 35):
			gcopy = gcopy[:-1]
			gtext = Album._list_to_str(gcopy)
		fontSize = int(round(IMAGE_WIDTH / 18))
		# if len(self.get_genres_as_str()) > 35:
		# 	fontSize = int(round(IMAGE_WIDTH * 35 / 18 / len(self.get_genres_as_str())))
		ttf = ImageFont.truetype(os.path.join("Arial-Unicode-Bold.ttf"), fontSize)
		I1.text((0, int(round(.75*extra_height))), gtext, (180, 180, 180), font=ttf)

		new_img = Image.new("RGBA", (IMAGE_WIDTH, extra_height + h))
		new_img.paste(pil_image, (0, 0))
		new_img.paste(background, (0, h))

		pil_image = new_img
		png_bio = io.BytesIO()
		pil_image.save(png_bio, format="PNG")
		png_data = png_bio.getvalue()

		return png_data

	@staticmethod
	def _get_rating(rating):
		res = int(100*(4.24 * float(rating) - 7.89))/100.
		if res < 0:
			res = 0.0
		if res > 10:
			res = 10.0
		return str(res)

	@staticmethod
	def _list_to_str(lst):
		res = ''
		for s in lst:
			res += s + ', '
		return res[:-2]