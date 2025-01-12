from flask import render_template, Blueprint
from singleton import Manga, Chapter, get_manga

bp = Blueprint('user', __name__)

@bp.route('/library')
def library():
    return render_template('library.html', title='Library')

@bp.route('/manga/<id>')
def manga_info(id):
    manga: Manga = get_manga(id)
    return render_template('manga.html', title=f'Manga {manga.title}', manga=manga)

@bp.route('/read/<manga>/<chapter>')
def read(manga, chapter):
    cur_manga: Manga = get_manga(manga)
    [cur_chapter] = filter(lambda ch: ch.id == chapter, [ ch for ch in cur_manga.chapters() ])
    return render_template('read.html', title=f'Read {cur_manga.title} {cur_chapter.number}', chapter=cur_chapter)