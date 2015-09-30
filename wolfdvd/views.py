# -*- coding: utf-8 -*-
import os
import sqlite3
import pickle
from import_list import load_db
from wolfdvd     import app
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
titles = pickle.load(open('./wolfdvd/static/tits_protected.pckl','r'))
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

@app.route('/add_entry', methods=['GET','POST'])
def add_entry():
# titles.append(re)
  if request.method=='POST':
    film = {}
    film['wolfloc']  = request.form['wolfloc']
#    film['director'] = request.form['director']
#    film['title']    = request.form['title']
    film['imdbid']   = request.form['imdbid']
#    film['year']  = '1998'
    return render_template('film.html', film=film)
  else:
    return render_template('add_movie.html')
#return render_template('add_movie.html')

if __name__=='__main__':
  app.run()

#These routes are to view linked to the SQL-database 
#might want to migrate there eventually, 
#currently just using pickled dictionary
#@app.route('/movies')
#def show_entries():
#  db = get_db()
#  cur = db.execute('select title, text from entries order by id desc')
#  entries = cur.fetchall()
#  return render_template('show_entries.html', entries=entries)
#@app.route('/add', methods=['POST'])
#def add_entry():
#  if not session.get('logged_in'):
#    abort(401)
#  db = get_db()
#  db.execute('insert into entries (title,text) values (?,?)',
#              [request.form['title'], request.form['text']])
#  db.commit()
#  flash('New entry was successfull posted')
#  return redirect(url_for('show_entries'))
