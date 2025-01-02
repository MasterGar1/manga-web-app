import os

import requests
import dotenv
from flask import Flask, render_template, redirect, url_for, session

import search

app = Flask(__name__)
app.register_blueprint(search.bp, url_prefix='/search')  # Ensure blueprint is registered with a prefix

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/library')
def library():
    return render_template('library.html', title='Library')

@app.route('/read/<manga>/<chapter>')
def read(manga, chapter):
    return render_template('read.html', title=f'Read {manga} {chapter}', chapter=[])

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if username in users and check_password_hash(users[username], password):
#             session['username'] = username
#             flash('Login successful!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid username or password', 'danger')
    
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('Logged out successfully!', 'success')
#     return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)



# dotenv.load_dotenv()
# base_url = 'https://api.mangadex.org'

# endpoint = '/manga'

# params = {
#     'title' : 'Strongest',  
#     'limit' : 10,         
#     'order[relevance]' : 'desc'  
# }

# creds = {
#     'grant_type': 'password',
#     'username': 'Gar1',
#     'password': os.getenv('PASSWORD'),
#     'client_id': os.getenv('CLIENT_ID'),
#     'client_secret': os.getenv('CLIENT_SECRET')
# }

# r = requests.post(
#     'https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token',
#     data=creds
# )
# r_json = r.json()

# headers = {
#     'Authorization': f'Bearer {r_json['access_token']}'
# }

# api_response = requests.get(base_url + endpoint, headers=headers, params=params)

# resp_dict = api_response.json()

# titles = [el['attributes']['title']['en'] for el in resp_dict['data']]

# print(titles, flush=True)