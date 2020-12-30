import settings
import pickle
import random
from bottle import request, response

r = settings.r

_randomSamples = 'abcdefghijklmnopqrstuvwxyz0123456789'
_defaultSessionName = 'gsid'
_defaultTimeout = 30 * 60

class Session(dict):
    def __init__(self, request:request, response:response, name=_defaultSessionName, timeout=_defaultTimeout):
        self.request =  request
        self.response = response
        self._name = name
        self._timeout = timeout
        self._new = True
        self._invalid = False
        dict.__init__(self)

        sid = request.cookies.get(self._name)
        if sid:
            self._sid = sid
            data = r.get(self._sid)
            if data:
                self.update(pickle.loads(data))
                r.set(self._sid, data)
                r.expire(self._sid, self._timeout)
                self._new = False
                return

        sid = ''.join([random.choice(_randomSamples) for i in range(8)])
        self._sid = sid
        self.response.set_cookie(self._name, self._sid, path='/')

    def save(self):
        if not self._invalid:
            r.set(self._sid, pickle.dumps(self.copy()))
            r.expire(self._sid, self._timeout)

    def is_new(self):
        return self._new

    def invalided(self):
        self.response.set_cookie(self._name, '', expires=-100)
        r.delete(self._sid)
        self.clear()
        self._invalid = True