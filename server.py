from flask import Flask
from flask import render_template, redirect, url_for,flash
from flask import request
import os
from flaskext.mysql import MySQL
from flask import send_from_directory
#from web.orm import *
from datetime import datetime
from flask_wtf.csrf  import CSRFProtect, CSRFError
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='123456789'
app.config['MYSQL_DATABASE_DB']='crudflask'
mysql.init_app(app)
carpeta= os.path.join("uploads")

app.config['carpeta']=carpeta
app.secret_key="biblioteca"
csrf=CSRFProtect(app)
@app.route('/')
def index():
    sql="select * from book;"
     
    conn =mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    books=cursor.fetchall()
     
    conn.commit()
    return render_template('book/index.html', books=books)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn =mysql.connect()
    cursor=conn. cursor()
   
    cursor.execute("select foto from book where id=%s",id)
    fila=cursor.fetchall()
    print("eliminando"+ app.config['carpeta'],fila[0][0])
    os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
    cursor.execute("delete from book where id=%s",(id))
    conn.commit()
    return redirect('/')

#actualización de usuarios
@app.route('/update', methods=[ 'POST'])
def update():
    
    conn =mysql.connect()
    cursor=conn. cursor()

    _autor=request.form.get('autor')
    _genero= request.form.get('genero')
    
    _id= request.form.get('id')
    _foto= request.files['foto']

    if _autor=='' or _genero=='' or id=='':
        flash('Hay campos incompletos')
        return redirect(url_for('edit',id))
    sql="update book set autor=%s, genero=%s, create_date=%s where id=%s"
    now =datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)
        cursor.execute("select foto from book where id=%s",_id)
        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['carpeta'],fila[0][0]))
         
        cursor.execute("update book set foto=%s where id =%s",(nuevoNombreFoto,_id))
        conn.commit()
      #  2022101418

    tiempo= now.strftime("%Y-%m-%d")
      
   # sql="insert into book(id,autor,genero, create_date, foto)values(null,%s,%s,%s,%s);"
    datos=(_autor,_genero, tiempo,_id)
    cursor.execute(sql,datos)
    conn.commit()
    #addbook(_autor, _genero)

    return redirect('/')

@app.errorhandler(CSRFError)
def handler_csrf_error(e):
    flash('intentas hackearme?','error')
    return render_template('book/index.html', reason= e.description),400
#ediccion de  books
@app.route('/edit/<int:id>')
def edit(id):
    conn =mysql.connect()
    cursor=conn. cursor()
    cursor.execute("select * from book where id=%s",(id))
    
    datos=cursor.fetchall()

    conn.commit()
    return render_template('book/edit.html',datos =datos)

#orquestador de imagenes
@app.route('/uploads/<namefoto>')
def uploads(namefoto):
    print("<<<<<<<")
    print("llego")
    print(namefoto)
    print(app.config['carpeta'],"img1.png")
    return send_from_directory(app.config['carpeta'],namefoto)




#almacenamiento de libros
@app.route('/store', methods=[ 'POST'])
def store():
    _autor=request.form.get('autor')
    _genero= request.form.get('genero')
    
    _foto= request.files['foto']
    now =datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        print("web/"+app.config['carpeta']+"/"+ nuevoNombreFoto)
        _foto.save("uploads/"+ nuevoNombreFoto)
    sql="insert into book(id,autor,genero, create_date, foto)values(null,%s,%s,%s,%s);"
    datos=(_autor,_genero, "2022-06-25",nuevoNombreFoto)
    conn =mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #addbook(_autor, _genero)

    return redirect('/')
@app.route('/create')
def create():
    #http://127.0.0.1:5000/params?params1=cristian
 
    return render_template('book/createbook.html')

if __name__ == '__main__':
    app.run(debug = True)
    