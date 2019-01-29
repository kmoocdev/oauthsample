# -*- coding: utf-8 -*-
from django.http import HttpResponse
import requests
from django.shortcuts import redirect
import urllib
import json
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt

client_id = 'xFxjX9M0qz8G0vzzUBiVjKwUSOQ2XUdGoCroHzdv'
client_secret = 'jmPj9avNYJR8oLFBhumjg7Lv08o67zAJkAKVmCvO2Isu0EcJCXrjcGCUVYozn8zbYytXp4XeQ5yfGxRaAmncdtHSheArCeXvlSB4bfqRTy5CTiODjLeJY1GWLqZwz95n'
access_token_url = 'http://all.kmooc.kr/o/token/'


@csrf_exempt
def test(request):
    """
    :param request:
    :return:

    시작 주소: http://all.kmooc.kr/accounts/login/?next=/o/authorize/%3Fclient_id%3DxFxjX9M0qz8G0vzzUBiVjKwUSOQ2XUdGoCroHzdv%26response_type%3Dcode
    """
    return HttpResponse(request.META)


def oauth2(request):
    authorization_url = 'http://all.kmooc.kr/o/authorize?'

    params = {
        'response_type': 'code',
        'client_id': 'xFxjX9M0qz8G0vzzUBiVjKwUSOQ2XUdGoCroHzdv'
    }

    authorization_url = authorization_url + urllib.urlencode(params)
    return redirect(authorization_url)


def complete(request):
    print 'request.META --- s'
    print request.META
    print 'request.META --- e'

    code = request.GET.get('code')

    print 'code:', code

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/complete/'

    }

    r = requests.post(access_token_url, data=data)
    print r.status_code, r.text

    response_json = json.loads(r.text)
    access_token = response_json.get('access_token')

    url = 'http://all.kmooc.kr/api/hello?' + urlencode({
        'access_token': access_token
    })

    str = requests.get(url)

    return HttpResponse(str.text)
