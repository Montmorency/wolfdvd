# -*- coding: utf-8 -*-
import os
import sqlite3
import pickle
from   import_list import load_db
from   wolfdvd     import app, import_imdb
from   flask       import Flask, request, session, g, redirect, url_for, abort,\
                          render_template, flash
from   imdb import IMDb
from   BeautifulSoup import BeautifulSoup
import urllib2


#titles is a list of dictionaries with keys
#wolfloc, title, director, imdbid
#this should be replaced by a decent database ORM
#for instance... peewee.

def check_db_integrity(titles):
	for title in titles:
		try:
			a = title['director']
		except KeyError:
			title['director'] = 'Unknown'
		try:
			a = title['wolfloc']
		except KeyError:
			title['wolfloc'] = 'WXXX'

def clean_db(titles):
	titles_wolfloc = {film['wolfloc']: film for film in titles}
	return titles_wolfloc

def find_imdb_ids(title):
	ia = IMDb()
	results = ia.search_movie(title)
	return results

@app.before_request
def before_request():
	f    = open(app.config['DATABASE'], 'r')
	g.db = pickle.load(f)
	f.close()

@app.teardown_request
def teardown_request(exception):
	f    = open(app.config['DATABASE'], 'w')
	pickle.dump(g.db, f)	
	f.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
      if request.form['username'] != app.config['USERNAME']:
          error = 'Invalid username'
      elif request.form['password'] != app.config['PASSWORD']:
          error = 'Invalid password'
      else:
          session['logged_in'] = True
          flash('You were logged in')
          return redirect(url_for('show_movies'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_movies'))

#Main Routes: DVD list, invidual page layout, adding to database
@app.route('/', methods=['GET', 'POST'])
def show_movies():
  check_db_integrity(g.db)
  sort_key = request.args.get('sort', 'wolfloc')
  if sort_key not in {'wolfloc', 'title', 'director'}:
    return abort(500, "Invalid sort key")
  titles_sorted = sorted(g.db, key=lambda x: x[sort_key])
  return render_template('show_movies.html', titles=titles_sorted)

@app.route('/movies/<wolfloc>')
def show_spec_movie(wolfloc):
	titles_wolfloc = clean_db(g.db)
	film = titles_wolfloc[wolfloc]
	ia = IMDb()
	try:
		movie = ia.get_movie(film['imdbid'])
		if 'cover url' in movie.keys():
			film['img']   = movie['cover url']
#Grab film pic if it isnt in the database already.
			if os.path.isfile('./wolfdvd/static/images/{0}.jpg'.format(wolfloc)):
				pass
			else:
				img = urllib2.urlopen(film['img'])
				with open('./wolfdvd/static/images/{0}.jpg'.format(wolfloc), 'w') as f:
					f.write(img.read())
			film['plot']  = movie.get('plot outline')
			film['url']   = ia.get_imdbURL(movie)
		else:
			print 'no cover_url'
			film['img']='http://www.englandfootballonline.com/images/Books/WrightFoot.JPG'	
			film['plot'] = ''
	except KeyError:
			film['img'] = 'http://www.englandfootballonline.com/images/Books/WrightFoot.JPG'	
			film['plot'] = ''
		#urlObj = urllib.urlopen(movie['cover url'])
		#imageData = urlObj.read()
		#urlObj.close()
	return render_template('film.html', film=film)


@app.route('/_modify_db/')
def modify_db()
	pass

#This view loops over titles in the database:
@app.route('/modify_title/<wolfloc>', methods=['GET', 'POST'])
def modify_title(wolfloc):
	titles_wolfloc = clean_db(g.db)
	film = titles_wolfloc[wolfloc]
	ia = IMDb()
 	s_results = ia.search_movie(film['title'])
	#s_results = []
	print s_results
	films = []
	for result in s_results:
		film = {}
		print result
		film['title']  = result['title']
		film['imdbid'] = result.movieID
		film['url']    = ia.get_imdbURL(result)
		movie = ia.get_movie(film['imdbid'])
		film['plot']   = movie.get('plot outline')
		films.append(film)
	if request.method=='POST':
# I suppose the logic here is the ajax query
		return redirect(url_for('show_spec_movie', wolfloc))
	else:
		return render_template('modify_title.html', films=films)

new_titles={}
#enter the wolflocation and imdbid of the title
@app.route('/add_entry', methods=['GET','POST'])
def add_entry():
	if request.method=='POST':
		film = {}
		film['wolfloc']  = request.form['wolfloc']
		film['imdbid']   = request.form['imdbid']
		new_titles[film['wolfloc']] = film['imdbid']
#Save a static copy of the new_titles dictionary.
#		update on the fly
		locations = [title['wolfloc'] for title in g.db]
		if film['wolfloc'] not in locations:
		#append new film instance
			import_imdb.imdb_to_dict(new_titles, g.db)
		else:
			flash('That wolfson location is already taken!')
		return render_template('add_movie.html')
	else:
		return render_template('add_movie.html')


@app.route('/remove_entry', methods=['GET','POST'])
def remove_entry():
	if request.method=='POST':
		wolfloc = request.form['wolfloc']
		locations = [title['wolfloc'] for title in g.db]
		if wolfloc in locations:
			g.db = [title for title in g.db if title['wolfloc'] != wolfloc]
			flash('Title removed')
		else:
			flash('That wolfloc is not in the library database.')
	return render_template('remove_movie.html')

if __name__=='__main__':
  app.run()
