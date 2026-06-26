from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/item_name')
def item_name():
    item_name= ERD .db("SELECT id, name from item")
    return render_template ('item_name.html', item_name=item_name)

@app.route('/item_name/<int:id>')
def singe_item_name(id):
    sql= f"SELECT* FROM item_name WHERE id={id}" #TOOO remove f-string
    item_name = ERD .db(sql, one=True)
    return render_template('single_item_name.html', item_name=item_name)

@app.route('/index/<int:id>')
def index(id):
    sql= f"SELECT* FROM index WHERE id={id}" #TOOO remove f-string
    index = ERD .db(sql, one=True)
    return render_template('index.html', index=index)

if __name__ == "__main__":
    # Hot reload using live server
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/")
    server.serve(
        port=5000,
        liveport=35729,
        debug=True
    )


