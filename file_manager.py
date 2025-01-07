from singleton import User
import json

import os

current_user : User = None

def choose_user(username : str) -> None:
    global current_user
    users = load_users()
    current_user = [ usr for usr in users if usr.username == username ]

def load_users() -> list[User]:
    dirs : list[str] = os.listdir('users')
    if len(dirs) == 0: return []
    users : list[User] = []
    for itm in dirs:
        with open(os.path.join('users', itm)) as file:
            usr : dict = json.load(file)
            users.append(User(usr))
    return users

def get_name_pass() -> dict[str, str]:
    users : list[User] = load_users()
    return { usr.username:usr.password for usr in users }

def save_user(user : User) -> None:
    with open(os.path.join('users', user.username + '.json'), 'x') as file:
        json_obj = json.dumps(user.to_dict())
        file.write(json_obj)