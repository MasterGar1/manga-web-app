from flask import render_template, Blueprint, session, Response, request

from singleton import Manga, User, get_manga, make_request, Chapter
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
    chapters: list[Chapter] = cur_manga.chapters()
    [cur_chapter] = [ ch for ch in chapters if ch.id == chapter]
    idx: int = chapters.index(cur_chapter)
    if idx == 0:
        [_, next_chapter] = chapters[idx:idx+2]
        prev_chapter = None
    elif idx == len(chapters) - 1:
        [prev_chapter, _] = chapters[idx-1:idx+1]
        next_chapter = None
    else:
        [prev_chapter, _, next_chapter] = chapters[idx-1:idx+2]
    update_user(session['username'], cur_manga, 
                {'current_chapter' : cur_chapter.number,
                'current_volume' : cur_chapter.volume})
    return render_template('read.html',
                           title=f'Read {cur_manga.title} {cur_chapter.number}',
                           manga=manga,
                           chapter=cur_chapter,
                           next=next_chapter,
                           prev=prev_chapter)

@bp.route('/image-proxy')
def image_proxy():
    url: str = request.args.get('url')
    response = make_request(url)
    return Response(response.content, content_type=response.headers['Content-Type'])