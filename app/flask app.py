from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_database.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    original_title = db.Column(db.String(100))
    overview = db.Column(db.Text)
    genre_ids = db.Column(db.Integer)

    def __repr__(self):
        return f'<Movie {self.title}>'

@app.route('/')
def index():
    return render_template('index.html')
