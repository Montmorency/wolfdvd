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

##Management Tool
This will launch the web app hosted locally and can be accessed through
your browser at http://127.0.0.1:5000/.

To add/remove new titles navigate to the view add/remove entry.
The only requirements for adding a title should be 
the Wolfloc (i.e. the WXXX number)
and the ID number of the film at the IMDb website. This is 
typically the digits at the end of the webpage describing the video
e.g.:

	http://www.imdb.com/title/tt0278500/

The ID would be 278500. These new additions 
are then automatically integrated into the
existing database.

##List Formatting
Tex files for printing pdf lists of the library can be generated using:
```   
   python import_list.py title_database.pckl 
```
This command will generate TeX files which can 
then be compiled in the usual way.


