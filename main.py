from flask import Flask, render_template, redirect, url_for, session
import dotenv
import os

import search
import login
import content

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(search.bp)
app.register_blueprint(login.bp)
app.register_blueprint(content.bp)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
