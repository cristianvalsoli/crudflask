from peewee import *
import datetime
from config import config

database=MySQLDatabase( config.get("DB_NAME"), host=config.get("DB_HOST"), port=config.get("DB_PORT"),user=config.get("DB_USER"), password=config.get("DB_PASSWORD"))




class book(Model):
    autor=CharField()
    genero=CharField()
    create_date=DateField(default=datetime.datetime.now)
    class Meta:
        database=database
        db_table="book"
if __name__=='__main__':


    if not book.table_exists():
        book.create_table()
        print ("instalado")
    else: print("ya instalado")
def addbook(autor, genero):
    try:
        new_book=book.create(autor=autor,genero=genero)
        #new_book.save()
    except DoesNotExist as e:
        return False
def uppdatebook(id,autor, genero):
    try:
             
        update_book = book.select().where(book.id== id).get()
        update_book.autor=autor
        update_book.genero=genero
       
        book.save() # Will do the SQL update query.
    except DoesNotExist as e:
        return False

def delete_book(id):

    try:
        update_book = book.select().where(book.id== id).get()
        update_book.delete()
        return True
        #SELECT A.name, T.name, A.floor FROM apartment as A join towers as T on A.tower= T.id;"
    except DoesNotExist as e:
        return False
addbook("Cristian", "Romance")

addbook("Ivan", "Acción")

addbook("Magaly", "Aventura")

addbook("Gilary", "Dramamys")