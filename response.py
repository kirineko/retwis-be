def response_json(code, msg, data):
    res = {
        'code': code,
        'msg': msg,
        'data': data
    }
    return res

def res_succ(data):
    return response_json(0, 'ok', data)


def res_fail(code, msg):
    return response_json(code, msg, '')