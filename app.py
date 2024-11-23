from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string
import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    __tablename__ = 'urls'  # Ensure the model is linked to your 'urls' table

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_key = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.TIMESTAMP, nullable=True)
    click_count = db.Column(db.Integer, default=0)

# Helper function to generate short keys
def generate_short_key():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_key = generate_short_key()
        new_url = URL(original_url=original_url, short_key=short_key)
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html', short_url=request.host_url + short_key)
    return render_template('index.html')

@app.route('/<short_key>')
def redirect_to_url(short_key):
    url = URL.query.filter_by(short_key=short_key).first_or_404()
    url.click_count += 1
    db.session.commit()
    return redirect(url.original_url)

if __name__ == '__main__':
    app.run(debug=True)
