"""Main file. Used to run the project."""
import os

from flask import Flask, render_template, redirect, url_for, session
import dotenv

import src.search as sc
import src.login as ln
import src.content as ct

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(sc.bp)
app.register_blueprint(ln.bp)
app.register_blueprint(ct.bp)

@app.route('/')
def home():
    """Home Page"""
    if 'username' in session:
        return render_template('index.html', title='Home')
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
