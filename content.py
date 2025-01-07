from flask import render_template, Blueprint
from singleton import Manga

bp = Blueprint('user', __name__)

@bp.route('/library')
def library():
    return render_template('library.html', title='Library')

@bp.route('/manga/<manga>')
def manga_info(manga):
    return render_template('manga.html', title=f'Manga {manga['title']}', manga=manga)

@bp.route('/read/<manga>/<chapter>')
def read(manga, chapter):
    return render_template('read.html', title=f'Read {manga} {chapter}', chapter=[])