"""Module containing the user related actions."""
from flask import render_template, Blueprint, session, Response, request, redirect

from .classes import Manga, User, Chapter, Library, Book, make_request
from .utility import get_genres, get_manga, split_words
from .file_manager import update_user, get_user, update_user_simple

bp = Blueprint('user', __name__)

@bp.route('/library/<query>')
def library(query: str):
    """Library page"""
    user: User = get_user(session['username'])
    lib: Library = user.library
    if query != 'none':
        sort, ordir, gen = query.split('+')
        lib.filter(gen)
        lib.sort(sort, ordir)
    genres: list[str] = ['Any'] + get_genres()
    return render_template('library.html', title='Library',
                           library=lib.books, order=Book.properties(),
                           genres=genres, word_split=split_words)

@bp.route('/manga/<manga_id>')
def manga_info(manga_id: str):
    """Info page"""
    manga: Manga = get_manga(manga_id)
    return render_template('manga.html', title=f'Manga {manga.title}', manga=manga)

@bp.route('/read/<manga>/<chapter>')
def read(manga: str, chapter: str):
    """Reading page"""
    cur_manga: Manga = get_manga(manga)
    chapters: list[Chapter] = cur_manga.chapters()
    [cur_chapter] = [ ch for ch in chapters if ch.id == chapter]
    idx: int = chapters.index(cur_chapter)
    if len(chapters) == 1:
        next_chapter = prev_chapter = None
    elif idx == 0:
        [_, next_chapter] = chapters[idx:idx+2]
        prev_chapter = None
    elif idx == len(chapters) - 1:
        [prev_chapter, _] = chapters[idx-1:idx+1]
        next_chapter = None
    else:
        [prev_chapter, _, next_chapter] = chapters[idx-1:idx+2]
    update_user(session['username'], cur_manga,
                {'current_chapter' : cur_chapter.number,
                'current_volume' : cur_chapter.volume,
                'favourite' : False})
    return render_template('read.html',
                           title=f'Read {cur_manga.title} {cur_chapter.number}',
                           manga=manga,
                           chapter=cur_chapter,
                           next=next_chapter,
                           prev=prev_chapter)

@bp.route('/remove-proxy/<manga_id>')
def remove_proxy(manga_id: str):
    """Proxy page to remove a manga from library"""
    user: User = get_user(session['username'])
    manga: Manga = get_manga(manga_id)
    if user.library.has(manga):
        user.library.remove(manga)
        update_user_simple(user)
    return redirect('/library/none')

@bp.route('/image-proxy')
def image_proxy():
    """Proxy image to generate images"""
    url: str = request.args.get('url')
    response = make_request(url)
    return Response(response.content, content_type=response.headers['Content-Type'])
