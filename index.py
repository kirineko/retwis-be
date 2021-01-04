import bottle
import settings
import time
import json
from convert import to_dict, to_list, to_set, to_string
from response import response_json, res_succ, res_fail
from model import User, Post, Timeline
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)
r = settings.r
login_user = None


@bottle.hook('after_request')
def enable_cors():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'


def auth(func):
    def api(*args, **kwargs):
        auth = bottle.request.query.auth
        if not auth:
            return res_fail(-1, 'need auth code to access')
        if not r.sismember('token', auth):
            return res_fail(-1, 'auth code error')

        try:
            user_data = cipher_suite.decrypt(auth.encode('utf-8'))
            user = json.loads(user_data.decode('utf-8'))
            global login_user
            login_user = User(user['uid'])
            return func(*args, **kwargs)
        except Exception as err:
            return res_fail(-1, "{}".format(err))
        
    return api


@bottle.get('/')
@auth
def index():
    user = login_user
    res = {
        'username': user.username,
        'posts': user.timeline(),
        'followers': user.followers(),
        'following': user.following(),
        'followers_num': user.followers_num(),
        'following_num': user.following_num()
    }
    return res

@bottle.get('/timeline')
@auth
def timeline():
    res = {
        'username': login_user.username,
        'posts': Timeline.posts(),
        'users': User.users()
    }
    return res


@bottle.get('/<username>')
@auth
def profile(username):
    user = User.find_by_username(username)
    if user and login_user:
        res = {
            'username': user.username,
            'loginname': login_user.username,
            'followers': user.followers(),
            'following': user.following(),
            'followers_num': user.followers_num(),
            'following_num': user.following_num(),
            'posts': user.posts(),
            'isfollowing': login_user.isfollowing(user)
        }
        return res

    return res_fail(-1, 'user not exist')

@bottle.get('/<loginname>/follow/<username>')
@auth
def follow(loginname, username):
    login_user = User.find_by_username(loginname)
    user = User.find_by_username(username)
    if login_user and user:
        login_user.add_following(user)
        return res_succ('')
    return res_fail(-1, 'user cannot find')

@bottle.get('/<loginname>/unfollow/<username>')
@auth
def unfollow(loginname, username):
    login_user = User.find_by_username(loginname)
    user = User.find_by_username(username)
    if login_user and user:
        login_user.remove_following(user)
        return res_succ('')
    return res_fail(-1, 'user cannot find')

@bottle.get('/mentions/<username>')
@auth
def mentions(username):
    user = User.find_by_username(username)
    if login_user and user:
        res = {
            'username': user.username,
            'loginname': login_user.username,
            'isfollowing': login_user.isfollowing(user),
            'posts': user.mentions()
        }
        return res
    
    return res_fail(-1, 'user not exist')


@bottle.post('/signup')
def sign():
    username = bottle.request.POST['username']
    password = bottle.request.POST['password']

    user = User.create(username, password)

    if (not user):
        return res_fail(-1, 'user created failed')

    user_data = {
        'uid': user.id,
        'username': user.username
    }
    auth_token = cipher_suite.encrypt(json.dumps(user_data).encode('utf-8')).decode('utf-8')
    r.sadd('token', auth_token)

    return res_succ({
        'auth': auth_token,
        'user': user_data
    })


@bottle.post('/login')
def login():
    username = bottle.request.POST['username']
    password = bottle.request.POST['password']

    user = User.find_by_username(username)
    if not user:
        return res_fail(-1, 'user not exist')
    
    if user.password != password:
        return res_fail(-1, 'password error')

    user_data = {
        'uid': user.id,
        'username': user.username
    }
    auth_token = cipher_suite.encrypt(json.dumps(user_data).encode('utf-8')).decode('utf-8')
    r.sadd('token', auth_token)
    return res_succ({
        'auth': auth_token,
        'user': user_data
    })
    

@bottle.get('/logout')
@auth
def logout():
    auth_token = bottle.request.query.auth
    r.srem('token', auth_token)
    return res_succ('')


@bottle.post('/post')
@auth
def post():
    user = login_user
    if user:
        content = bottle.request.POST['content']
        post = Post.create(user, content)
        return post.__dict__
    else:
        return res_fail(-1, 'user need auth')

bottle.run(reloader=True, port=8082)


