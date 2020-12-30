import bottle
import settings
import session
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
            print(login_user)
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
    user = islogin()
    if user:
        res = {
            'username': user.username,
            'posts': Timeline.posts(),
            'users': User.users()
        }
        return res

    bottle.redirect('/')

@bottle.get('/<username>')
@bottle.view('profile')
def profile(username):
    login_user = islogin()
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
    
    bottle.redirect('/')

@bottle.get('/<loginname>/follow/<username>')
def follow(loginname, username):
    login_user = User.find_by_username(loginname)
    user = User.find_by_username(username)
    if login_user and user:
        login_user.add_following(user)
        bottle.redirect('/{}'.format(user.username))
    bottle.redirect('/')

@bottle.get('/<loginname>/unfollow/<username>')
def unfollow(loginname, username):
    login_user = User.find_by_username(loginname)
    user = User.find_by_username(username)
    if login_user and user:
        login_user.remove_following(user)
        bottle.redirect('/{}'.format(user.username))
    bottle.redirect('/')

@bottle.get('/mentions/<username>')
@bottle.view('mentions')
def mentions(username):
    login_user = islogin()
    user = User.find_by_username(username)
    if login_user and user:
        res = {
            'username': user.username,
            'loginname': login_user.username,
            'isfollowing': login_user.isfollowing(user),
            'posts': user.mentions()
        }
        return res
    
    bottle.redirect('/')


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
def logout():
    sess = session.Session(bottle.request, bottle.response)
    sess.invalided()
    bottle.redirect('/')


@bottle.post('/post')
def post():
    user = islogin()
    if user:
        content = bottle.request.POST['content']
        Post.create(user, content)
        bottle.redirect('/')
    else:
        bottle.redirect('/signup')

@bottle.get('/public/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='public/')

bottle.run(reloader=True, port=8082)


