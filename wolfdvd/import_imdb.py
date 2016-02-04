import sys
import re
import imdb
import pickle
from datetime import datetime
from datetime import date
from import_list import Film, load_db, save_db, tit_sort, add_new_titles

def load_titles():
  tits = load_db('03-12-2013-1626.pckl')
  for i, tit in enumerate(tits):
    print i+1,'/',len(tits),tit.name
  return tits

# Pass this routine a list of new Wolfson
# locations and imdbids, then the title_database
# will be updated in place. new_titles
# is a dict title_database is a list of dicts.

def imdb_to_dict(new_titles, title_database):
  ia = imdb.IMDb()
  for i, (wolfloc, imdbid) in enumerate(new_titles.items()):
      title={}
      print i+1,'/', len(new_titles.items()), wolfloc
      try:
          movie = ia.get_movie('{0}'.format(imdbid))
          title['title']    = movie['title']
          title['wolfloc']  = wolfloc
          title['year']     = movie['year']
          title['director'] = movie['director'][0]['name']
          title['country']  = movie['countries'][0]
          title['imdbid']   = imdbid
      except:
          print tit.name
          print 'no imdb id number', tit.imdbid
          title['title']   = tit.name
          title['wolfloc'] = tit.wolfloc
      print title
      title_database.append(title)
  return

def dump_updated_db(titles):
  f = open('title_database_{0}.pckl'.format(date.today()),'w')
  pickle.dump(titles, f)
  f.close()
  
if __name__=='__main__':
#ToRun:
#python import_imdb.py ./new_titles.pckl ./title_database.pckl
#generates updated database in format ./title_database_{date}.pckl
  print 'sysargv', sys.argv[1], sys.argv[2]
  f,g = sys.argv[1], sys.argv[2]
  new_titles     = pickle.load(open(f,'r'))
  title_database = pickle.load(open(g,'r'))
  print len(title_database)
  print title_database[-5:]
  imdb_to_dict(new_titles, title_database)
  dump_updated_db(title_database)
