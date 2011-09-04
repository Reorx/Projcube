import re
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate as auth_authenticate

from utils.viewsbase import render_tpl, ApiBaseError, get_rsrc

def validate(val, p, unique=None):
    res = re.search(p, val)
    if res:
        return True
    else:
        raise ValueError

def _login(req, username, password):
    user = auth_authenticate(
            username = username,
            password = password)
    auth_login(req, user)

def signup(req, tpl='accounts/signup.html'):
    if 'POST' == req.method:
        dataFields = ['username', 'password1', 'password2',
                    'email']
        postData = req.POST.copy()

        # validate post data
        if len(dataFields) != len(postData):
            raise ApiBaseError(400, 'Post Data Not Complete')
        for i in dataFields:
            if not i in postData:
                raise ApiBaseError(400, 'Post Data Not Complete')
        try:
            validate(postData['username'], '^[\w]{4,16}$')
            validate(postData['email'], '^[\w\.]+@[\w]+\.[a-zA-Z]+$')
            validate(postData['password1'], '^.{4,32}$')
            validate(postData['password2'], '^.{4,32}$')
        except ValueError:
            raise ApiBaseError(400, 'Post Data Invalid')
        if not postData['password1'] == postData['password2']:
            raise ApiBaseError(400, 'Password Not Equal')
        try:
            u = User.objects.get(username=postData['username'])
        except:
            u = None
        if u:
            raise ApiBaseError(400, 'username or email already exist')
        try:
            u = User.objects.get(email=postData['email'])
        except:
            u = None
        if u:
            raise ApiBaseError(400, 'username or email already exist')
        
        # create user
        new_user = User.objects.create_user(
                postData['username'], postData['email'], postData['password1'])
        new_user.save()

        _login(req, postData['username'], postData['password1'])

        return HttpResponseRedirect('/')

    else:
        return render_tpl(req, tpl)

def logout(req):
    from django.contrib.auth import logout
    logout(req)
    return HttpResponseRedirect('/accounts/login')
