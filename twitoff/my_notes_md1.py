from flask import Flask, render_template
from .models import DB,User , Tweet

# main code
# def create_app():
# initializes our app
app = Flask(__name__)
# Database configurations
# app.config["SQLALCHEMY_DATA_URI"] = 'sqlite:///db.sqlite3'
# app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# listen to a "route"
# using decorater @
# '/' is the home page route
@app.route('/')
def root():
    # what i want ot happen when somebody goes to home page
    # return "Hello World!"
    return render_template('base.html',tite ="Home")
    # return render_template('base.html',tite ="Bananas")

# add other route
@app.route('/test')
def test():
    return "Another page"

# app title

app_title = "Twitoff DS32"
@app.route('/test')
def test():
    return f"A page from the {app_title}.app"

# kind of like what Jinja2 does  to our web pages
app_title = "Twitoff DS32"
@app.route('/test')
def test():
    return f"A page from the {app_title}.app"

@app.route('/hola')
def hola():
        return "Hola, Twitoff!"

    # return our app object after attaching the routes to it.
    return app  




  

