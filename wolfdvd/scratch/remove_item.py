import sys
import pickle

#location to remove
wolfloc = sys.argv[1]
f = open(sys.argv[2],'r')
title_db  = pickle.load(f)
f.close()
new_db = [title for title in title_db if title['wolfloc'] != wolfloc]

f = open(sys.argv[2], 'w')
pickle.dump(new_db,f)
f.close()



