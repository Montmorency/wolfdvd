`WolfFDVD` is a Python/Flask framework for managing and accessing 
the Wolfson College DVD library.

The package is developed and supported by:
  - Henry Lambert

## Dependencies:
  - [IMDbPY](http://imdbpy.sourceforge.net/)
  - [Flask](http://flask.pocoo.org/)


##Quick Start

0. git clone  https://github.com/Montmorency/wolfdvd

1. Initialize the WolfDVD app:
```
    python runserver.py 
```

This will launch the web app hosted locally and can be accessed through
your browser at http://127.0.0.1:5000/.

To add new titles navigate to the view Passing the Films 
Location and IMDBid. Navigate to http://127.0.0.1:5000/add_entry.
The only requirements should be the Wolfloc (i.e. the WXXX number)
and the ID number of the IMDb webstite typically the digits
at the end of the webpage describing the video:

	http://www.imdb.com/title/tt0278500/

This produces a file: 
    new_titles.pckl

These new additions are then integrated into the
existing database using:
```
    python import_imdb.py new_titles.pckl title_database.pckl
```
Tex files for printing pdf lists of the library can be generated using:
```   
   python import_list.py title_database.pckl 
```

