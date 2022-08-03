from PIL import Image
import cloudscraper
import io

class Album:
	def __init__(self, name, artists, rating, genres, link):
		self.name = name
		self.artists = artists
		self.rating = Album._get_rating(rating)
		self.genres = genres
		self.link = 'https://' + link

	def __str__(self):
		artists = ''
		for artist in self.artists:
			artists += artist + ", "
		artists = artists[:-2]

		genres = ''
		for genre in self.genres:
			genres += genre + ", "
		genres = genres[:-2]

		return self.name + "\n" + artists + "\n" + self.link + "\n" + genres + '\n' + self.rating

	def get_png_data(self):
		if self.link.rstrip() != 'https://':
			url = self.link
		else:
			url = 'https://e.snmc.io/i/600/s/8559a4fc4072bf4049920706e223a5af/8703155/critarc-x-jumbudrif-this-image-is-blocked-either-due-to-legal-restrictions-in-your-country-or-due-to-your-personal-settings-login-and-go-to-your-account-options-to-see-more-info-Cover-Art.jpg'
		jpg_data = (
			cloudscraper.create_scraper(
				browser={"browser": "firefox", "platform": "windows", "mobile": False}
			)
			.get(url)
			.content
		)

		pil_image = Image.open(io.BytesIO(jpg_data))

		basewidth = 298
		wpercent = (basewidth/float(pil_image.size[0]))
		hsize = int((float(pil_image.size[1])*float(wpercent)))
		pil_image = pil_image.resize((basewidth,hsize), Image.ANTIALIAS)
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
