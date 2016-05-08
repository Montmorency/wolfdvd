import pickle
import sys

def update_plot():
#pass wolfloc and the plot as a txt file with the plot
#written in to it
	wolfloc     = sys.argv[1]
	plot_string = open(sys.argv[2],'r').read()
	print plot_string
	with open('./static/tits_protected.pckl', 'r') as db:
		gdb = pickle.load(db)
	for title in gdb:
		if title['wolfloc'] == wolfloc:
			title['plot'] = plot_string
	with open('./static/tits_protected.pckl','w') as db:
		pickle.dump(gdb, db)

if __name__=='__main__':
#	update_plot()
	with open('./static/tits_protected.pckl', 'r') as db:
		gdb = pickle.load(db)
	wolfloc = sys.argv[1]
	for title in gdb:
		if title['wolfloc'] == wolfloc:
			print title
