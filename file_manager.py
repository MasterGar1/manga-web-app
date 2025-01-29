from singleton import User, encrypt, Manga

import json
import os

def get_name_pass() -> dict[str, str]:
    users : list[User] = load_users()
    return { usr.username:usr.password for usr in users }

def load_users() -> list[User]:
    dirs: list[str] = os.listdir('users')
    if len(dirs) == 0: return []
    users: list[User] = []
    for itm in dirs:
        with open(os.path.join('users', itm), 'r') as file:
            usr: dict = json.load(file)
            users.append(User(usr))
    return users

def save_user(user: User) -> None:
    with open(os.path.join('users', encrypt(user.username) + '.json'), 'x') as file:
        json_obj = json.dumps(user.to_dict())
        file.write(json_obj)

def get_user(name: str) -> User:
    enc_name: str = encrypt(name)
    dirs: list[str] = [ itm for itm in os.listdir('users') 
                        if itm.removesuffix('.json') == enc_name ]
    if len(dirs) == 0: return None

    with open(os.path.join('users', dirs[0]), 'r') as file:
        usr: dict = json.load(file)
        return User(usr)

def delete_user(name: str) -> None:
    pth: str = os.path.join('users', encrypt(name) + '.json')
    if os.path.exists(pth):
        os.remove(pth)

def update_user(name: str, manga: Manga, chapter: int) -> None:
    user: User = get_user(name)
    user.update(manga, chapter)
    delete_user(name)
    if not user is None:
        save_user(user)

def update_user_simple(user: User) -> None:
    if not user is None:
        delete_user(user.username)
        save_user(user)