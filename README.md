Python/Flask framework for generating latex list of DVDs in Wolfson
DVD library, and linking titles to IMDb website.

DEPENDENCIES:
Requires the IMDbPY library which can be found here:
  http://imdbpy.sourceforge.net/


New additions can be added using the web_interface. Passing the Films
Location and IMDBid. 

This produces a file new_titles.pckl

These new additions are then integrated into the
existing database using:
  python ./import_imdb.py ./new_titles.pckl ./title_database.pckl

The tex files for printing the pdfs in the lodge are generated using
  python ./import_list.py ./title_database.pckl 


