Python/Flask framework for generating list of DVDs in Wolfson
DVD library, and linking titles to IMDb website.

New additions can be added using the web_interface. Passing the Films
Location and IMDbid. This produces a file new_titles.pckl

These new additions are then integrated into the
existing database using:
  python ./import_imdb.py ./new_titles.pckl ./title_database.pckl

The tex files for printing the pdfs in the lodge are generated using
  python ./import_list.py ./title_database.pckl 
