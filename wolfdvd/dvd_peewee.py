from peewee import *

db = SqliteDatabase('movies.db') 
class BaseModel(Model):
  class Meta:
    database = database

class Film(BaseModel):
  title    = CharField()
  director = CharField()
  wolfloc  = CharField()
  synopsis = CharField()
  imdbid   = IntegerField()

class Relationship(BaseModel):
  from_film = ForeignKeyField(Film, related_name='relationships')
  to_film   = ForeignKeyField(Film, related_name='related_to')
  class Meta:
    indices = (
              (('from_film', 'to_film'), True),
              )

class FilmNote(BaseModel):
  film = ForeignKeyField(Film, related_name='pets')
  notes = CharField()

