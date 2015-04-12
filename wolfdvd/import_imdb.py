import sys
from import_list import Film, load_db, save_db, tit_sort, add_new_titles
import pickle
import re
from datetime import datetime
import imdb

def load_titles():
  tits = load_db('03-12-2013-1626.pckl')
  for i, tit in enumerate(tits):
    print i+1,'/',len(tits),tit.name
  return tits

def imdb_to_dict():
  ia = imdb.IMDb()
  tits_list_dict = []
  for i, tit in enumerate(tits):
      title ={}
      print i+1,'/', len(tits), tit.name
      try:
          movie = ia.get_movie('%s'%tit.imdbid)
          title['title']    = movie['title']
          title['wolfloc']  = tit.wolfloc
          title['year']     = movie['year']
          title['director'] = movie['director'][0]['name']
          title['country']  =  movie['countries'][0]
          title['imdbid']   =  tit.imdbid
      except:
          print tit.name
          print 'no imdb id number', tit.imdbid
          title['title']    = tit.name
          title['wolfloc']  = tit.wolfloc
          title['imdbid']   =  0

      tits_list_dict.append(title)
  for tit in tits_list_dict:
      print tit.values()
  return tits_list_dict

def dump_updated_db(tits_list):
  f = open('tits_list_dict1.pckl','w')
  pickle.dump(tits_list, f)
  f.close()
  
if __name__=='__main__':
  #db = sys.argv[1]
  tits = load_titles()
  tits_list = imdb_to_dict(tits[1:5])
  #tits_list = load_titles(db)
  dump_updated_db(tits_list)
   
