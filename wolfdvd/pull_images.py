# -*- coding: utf-8 -*-
import os
import json
import pickle
import urllib2
import sqlite3

from imdb          import IMDb
from BeautifulSoup import BeautifulSoup
from import_list   import load_db
from flask         import Flask, request, session, g, redirect, url_for, abort,\
                          render_template, flash
      
def get_film_image(film):     
  """
  :method:`get_film_image` pull image from url and save to static folder.
  """
  try:
    img = urllib2.urlopen(film['img'])
  except urllib2.HTTPError:
    ia = IMDb()
    movie = ia.get_movie(film['imdbid'])
    film['img']   = movie['cover url']
    img = urllib2.urlopen(film['img'])

  img_name ='./static/images/{0}.jpg'.format(film['wolfloc']) 
  with open(img_name, 'w') as f:
	  f.write(img.read())

if __name__=="__main__":
  DATABASE='./static/tits_protected.pckl'
  f = open(DATABASE, 'r')
  film_db = pickle.load(f)
  for film_no, film in enumerate(film_db):
    print film_no, film
    try:
      film['img']
    except:
      with open('no_images.txt', 'a') as f:
        print >> f, film
    else:
      get_film_image(film)




