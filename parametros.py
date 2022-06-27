from flask import Flask
from flask import request
app = Flask(__name__)
@app.route('/')
def index():
    return 'Hola mundos2'


@app.route('/params')

@app.route('/params/<name>/')
def params( name="deberias agregar un name"):
    #http://127.0.0.1:5000/params?params1=cristian
    return 'El parametro es :,{}'.format(name)




if __name__ == '__main__':
    app.run(debug = True)
    