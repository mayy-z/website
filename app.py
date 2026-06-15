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

@app.route('/item/<int:id>')
def item(id):
    sql = "SELECT * FROM item WHERE id=?"
    item = query_db(sql,args=(id,),one=True)
    return render_template('item.html', item=item)

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


