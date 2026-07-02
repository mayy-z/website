from flask import Flask, render_template, request, flash, session, redirect
from livereload import Server
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True


def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect('ERD .db')
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results

@app.route('/')
def index():
    results = query_db("SELECT * FROM Item")  
    return render_template('index.html',results=results)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/item_name')
def item_name():
    item_name= ERD .db("SELECT id, name from item")
    return render_template ('item_name.html', item_name=item_name)

@app.route('/item/<int:id>')
def singe_item_name(id):
    sql= f"SELECT * FROM Item WHERE id={id}" #TOOO remove f-string
    item_name = query_db(sql, one=True)
    return render_template('single_item_name.html', item_name=item_name)

@app.route('/login', methods=["GET","POST"])
def login():
    #if the user posts a username and password
    if request.method == "POST":
        #get the username and password
        Name = request.form['Name']
        Password = request.form['password']
        #try to find this user in the database- note- just keepin' it simple so usernames must be unique
        sql = "SELECT * FROM user WHERE Name = ?"
        user = query_db(sql=sql,args=('Name',),one=True)
        if user:
            #we got a user!!
            #check password matches-
            if check_password_hash(user[2],Password):
                #we are logged in successfully
                #Store the username in the session
                session['user'] = user
                flash("Logged in successfully")
            else:
                flash("Password incorrect")
        else:
            flash("Username does not exist")
    #render this template regardles of get/post
    return render_template('login.html')

@app.route('/signup', methods=["GET","POST"])
def signup():
    #if the user posts from the signup page
    if request.method == "POST":
        #add the new username and hashed password to the database
        Name = request.form['Name']
        Password = request.form['Password']
        #hash it with the cool secutiry function
        hashed_Password = generate_password_hash(Password)
        #write it as a new user to the database
        sql = "INSERT INTO user (username,password) VALUES (?,?)"
        query_db(sql,(Name,hashed_Password))
        #message flashes exist in the base.html template and give user feedback
        flash("Sign Up Successful")
    return render_template('signup.html')

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


