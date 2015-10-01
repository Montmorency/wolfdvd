import sys
import re
import pickle
from datetime import datetime
from imdb import IMDb

class Film:
	def __init__(self):
		self.name     = ''
		self.name2    = ''
		self.wolfloc  = ''
		self.imdbid   = 0
		self.director = 'Anon'
		self.year	  = 0
	
	def __repr__(self):
		return repr((self.name, self.wolfloc, self.director, self.imdbid))

def print_preamble(mode):
	print >>f, '\documentclass{article}'
	print >>f, '\usepackage[english]{babel}'
	print >>f, '\usepackage[utf8]{inputenc}'
	print >>f, '\usepackage{longtable}'
	print >>f, '\usepackage[top=0.5in, bottom=0.5in, left=0.5in, right=0.5in]{geometry}'
	print >>f, '\\begin{document}'
	print >>f, '\\begin {center}'
	if mode==1:
		print >>f, '\\begin{longtable}{l p{10cm} l l}'
	elif mode==2:
		print >>f, '\\begin{longtable}{p{10cm} l l l}'
	elif mode==3:
		print >>f, '\\begin{longtable}{l p{10cm} l l}'
	print >>f, '\hline'
	print >>f, '\\\\'

def print_term():
	print >>f, '\hline'
	print >>f, '\end{longtable}' 
	print >>f, '\end{center}'
	print >>f, '\end{document}'

def gen_list(titles, mode):
	print_preamble(mode)
	for title in titles:
		title_name = title['title']
		if '&' in title_name:
			title_name = title_name.replace('&','\&')
		if '_' in title_name:
			title_name = title_name.replace('_','\_')
		try:
				if mode==1:
					print >>f, "%s & %s & %s & %s \\\\"%(title['wolfloc'].encode('utf-8'), title_name.encode('utf-8'), title['director'].encode('utf-8'), title['year'])
				elif mode==2:
					print >>f, "%s & %s & %s & %s \\\\"%(title_name.encode('utf-8'), title['wolfloc'].encode('utf-8'), title['director'].encode('utf-8'), title['year'])
				elif mode==3:
					print >>f, "%s & %s & %s & %s \\\\"%(title['director'].encode('utf-8'), title_name.encode('utf-8'), title['wolfloc'].encode('utf-8'), title['year'])
				else:
					print 'come on you better than that.'
		except KeyError:
				if mode==1:
					print >>f, "%s & %s & %s & %s \\\\"%(title['wolfloc'], title_name,'','')
				elif mode==2:
					print >>f, "%s & %s & %s & %s \\\\"%(title_name, title['wolfloc'] ,'','')
				elif mode==3:
					print >>f, "%s & %s & %s & %s \\\\"%('', title_name, title['wolfloc'], '')
				else:
					print 'come on you better than that.'
	print_term()


def find_imdb_ids(tits, ia):
#ia is imdb.IMDb() object
	for tit in tits:
		s_results = ia.search_movie(tit.name)
		for result in s_results:
			try:
				print result['title'], result['year'], result.movieID
			except KeyError:
				print result['title']
		#prompt for which title is the desired title
			a = raw_input('which num-->')
			if a=='':
				continue
			else:
				a = int(a)
				print a 
				tit.imdbid = s_results[a].movieID

def pop_database():
	f = open('back5.dat','r').read()
	title_re = re.compile(r'00-00-00-00.*?\n(.*?);\n\n', re.S)
	titles = title_re.findall(f)
	tits = []
	for title in titles:
		x = Film()
		a = title.split('\n')
		x.name    = a[0].split('|')[0] 
		x.name2   = a[0].split('|')[1] 
		x.wolfloc = a[1].split(';')[7] 
		x.imdbid  = a[2].split(';')[1] 
		#print x.title, x.wolfloc, x.imdbid
		tits.append(x)
	return tits

def load_db(db):
	f1 = open('%s'%db,'r')
	tits = pickle.load(f1)
	f1.close()
	return tits

def save_db(tits):
	a  = datetime.today()
	a  = a.strftime('%d-%m-%Y-%H%M')
	f1 = open('%s.pckl'%a,'w')
	pickle.dump(tits,f1)
	f1.close()

def new_titles():
#read any new titles from file new_titles format (name| wolfloc).
	f = open('new_titles','r')
	h = f.read().split('\n')
	f.close()
	tits = []
	for title in h:
		try:
			title = title.split('|')
			x = Film()
			x.name=title[0].strip()
			x.wolfloc=title[1].strip()
			tits.append(x)
		except:
			print 'end of file'
	return tits

def add_new_titles(tits):
	newtits = new_titles()
	for tit in newtits:
	    tits.append(tit)
	return tits

def tit_sort(tits):
		tits.sort(key=lambda title:title.wolfloc)
		return tits

def print_list():
#tits = pop_database()
 	f = open('tits_protected.pckl','r')
	tits = pickle.load(f)
	for tit in tits:	
		tit['wolfloc'] = tit['wolfloc'].strip()
	f.close()
	for i in range(1,4):	
  		f = open('wolf_list%s.tex'%(str(i)),'w')
		if i==1:
			tits.sort(key=lambda title:title.wolfloc)
			gen_list(tits,i)
		else:
			continue
		f.close()

if __name__=='__main__':
# Run this script as main to
# generate the tex files from a fresh
# pickle of the database.
# python import_list ./title_database.pckl
  f = open(sys.argv[1], 'r')
  tits = pickle.load(f)
#Hack for appending directors...
  for tit in tits:
    try:
      tit['director']
    except:
      tit['director']=''

  for tit in tits:	
    tit['wolfloc'] = tit['wolfloc'].strip()
    tit['director'] = tit['director'].strip()
    tit['title'] = tit['title'].strip()
	
  f.close()
  for i in range(1,4):	
    f = open('wolf_list%s.tex'%(str(i)),'w')
    if i==1:
      tits.sort(key=lambda title:title['wolfloc'])
      gen_list(tits,i)
    elif i==2:
      tits.sort(key=lambda title:title['title'])
      gen_list(tits,i)
    if i==3:
      tits.sort(key=lambda title:title['director'])
      gen_list(tits,i)
    f.close()
