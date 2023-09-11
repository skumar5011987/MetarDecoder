
from nws import settings

def get_url(scode='',ext=''):
    return settings.NWS_URL + scode + ext

def api_response(status=200, msg='', resp='',):
    return {
        'status': status,
        'message': msg,
        'results':{
            'data': resp
        }
    }