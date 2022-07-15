import random
import requests
import urllib.request
import numpy as np
import cv2

class Album:
	def __init__(self, name, artists, rating, genres, link):
		self.name = name
		self.artists = artists
		self.rating = Album._get_rating(rating)
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

	@staticmethod
	def _get_rating(rating):
		res = int(100*(4.24 * float(rating) - 7.89))/100.
		if res < 0:
			res = 0.0
		if res > 10:
			res = 10.0
		return str(res)