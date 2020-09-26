from flask_sqlalchemy import SQLAlchemy
# import flask app from app.py
import toml

config = toml.load('config.toml')

# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config["database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=True, nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(500), nullable=False)

    # def __repr__(self):
    #     return '<Title %r>' % self.title