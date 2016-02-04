The `WOLFDVD` is a Python/Flask framework for managing and accessing 
the Wolfson College DVD library.

The package is developed and supported by:
  -Henry Lambert

## Dependencies:
  -[IMDbPY library](http://imdbpy.sourceforge.net/)
  -[Flask](http://flask.pocoo.org/)


## Features


##Quick Start

0. git clone  https://github.com/Montmorency/wolfdvd

1. Initialize the WolfDVD app:
```
    python runserver.py 
```

  This will launch the web app hosted locally and can be accessed through
  your browser at http://127.0.0.1:5000/.


To add new titles navigate to the view Passing the Films Location and IMDBid.
If you are running through a local server the address 
would be http://127.0.0.1:5000/add_entry.


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

