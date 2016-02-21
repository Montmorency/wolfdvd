# -*- coding: utf-8 -*-
import os
import sqlite3
import pickle
from import_list import load_db
from wolfdvd     import app, import_imdb
from flask       import Flask, request, session, g, redirect, url_for, abort,\
                        render_template, flash

def connect_db():
  """Connects to the specific database."""
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv
  
def init_db():
  """Creates the database tables."""
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def get_db():
  if not hasattr(g,'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

#titles is a list of dictionaries with keys
#wolfloc, title, director, imdbid
#this should be replaced by a decent database ORM
#for instance... peewee.
title_db = './wolfdvd/static/tits_protected.pckl'
f = open(title_db,'r')
titles = pickle.load(f)
f.close()

for title in titles:
  try:
    title['director']
  except KeyError:
    title['director']="Unknown"
  try:
    title['imdbid']
  except:
    title['imdbid']=0
titles_wolfloc = {film['wolfloc']: film for film in titles}

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
  sort_key = request.args.get('sort', 'wolfloc')
  if sort_key not in {'wolfloc', 'title', 'director'}:
    return abort(500, "Invalid sort key")
  titles_sorted = sorted(titles, key=lambda x: x[sort_key])
  return render_template('show_movies.html', titles=titles_sorted)

@app.route('/movies/<wolfloc>')
def show_spec_movie(wolfloc):
  film = titles_wolfloc[wolfloc]
  return render_template('film.html', film=film)

new_titles={}
#enter the wolflocation and imdbid of the title
@app.route('/add_entry', methods=['GET','POST'])
def add_entry():
	global titles
	f = open('new_titles.pckl','w')
	if request.method=='POST':
		film = {}
		film['wolfloc']  = request.form['wolfloc']
		film['imdbid']   = request.form['imdbid']
		new_titles[film['wolfloc']] = film['imdbid']
#Save a static copy of the new_titles dictionary.
		pickle.dump(new_titles,f)
#		update on the fly
		locations = [title['wolfloc'] for title in titles]
		if film['wolfloc'] not in locations:
		#append new film instance
			db = open(title_db, 'w')
			import_imdb.imdb_to_dict(new_titles, titles)
			picle.dump(titles, db)
			db.close()
		else:
			flash('The wolfson location is already taken!')
		return render_template('add_movie.html')
	else:
		return render_template('add_movie.html')

@app.route('/remove_entry', methods=['GET','POST'])
def remove_entry():
	global titles
	global title_db
	if request.method=='POST':
		wolfloc = request.form['wolfloc']
		locations = [title['wolfloc'] for title in titles]
		if wolfloc in locations:
			titles = [title for title in titles if title['wolfloc'] != wolfloc]
			f = open(title_db, 'w')
			pickle.dump(titles, f)
			f.close()
			flash('Title removed')
		else:
			flash('That wolfloc is not in the library database')
	return render_template('remove_movie.html')

if __name__=='__main__':
  app.run()
