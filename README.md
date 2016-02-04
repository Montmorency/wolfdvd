Python/Flask framework for generating latex list of DVDs in Wolfson
DVD library, and linking titles to IMDb website.

DEPENDENCIES:
Requires the IMDbPY library which can be found here: http://imdbpy.sourceforge.net/
You must have Flask on your system http://flask.pocoo.org/.


New additions can be added using the web interface. This is initialized by
writing:
```
    python runserver.py 
```

This will launch the web app hosted locally and can be accessed through
your browser at http://127.0.0.1:5000/.


To add new titles navigate to the view Passing the Films Location and IMDBid. 
If you are running through a local server the address would be http://127.0.0.1:5000/add_entry

This produces a file: 
    new_titles.pckl

These new additions are then integrated into the
existing database using:
```
    python import_imdb.py new_titles.pckl title_database.pckl
```
The tex files for printing the pdfs in the lodge are generated using
```   
   python import_list.py title_database.pckl 
```

