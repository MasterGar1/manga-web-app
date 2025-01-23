from flask import render_template, Blueprint, session
from singleton import Manga, User, get_manga
from file_manager import update_user, get_user

bp = Blueprint('user', __name__)

@bp.route('/library')
def library():
    user: User = get_user(session['username'])
    return render_template('library.html', title='Library', library=user.library.books)

@bp.route('/manga/<id>')
def manga_info(id: str):
    manga: Manga = get_manga(id)
    return render_template('manga.html', title=f'Manga {manga.title}', manga=manga)

@bp.route('/read/<manga>/<chapter>')
def read(manga: str, chapter: str):
    cur_manga: Manga = get_manga(manga)
    [cur_chapter] = filter(lambda ch: ch.id == chapter,
                           [ ch for ch in cur_manga.chapters() ])
    update_user(session['username'], cur_manga, 
                {'current_chapter' : cur_chapter.number,
                'current_volume' : cur_chapter.volume})
    return render_template('read.html',
                           title=f'Read {cur_manga.title} {cur_chapter.number}',
                           manga=manga,
                           chapter=cur_chapter)