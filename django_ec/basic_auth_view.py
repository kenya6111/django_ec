import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def view_or_basicauth(view, request, test_func, realm="", *args, **kwargs):
    """
    ログイン済みかBasic認証が提供されているかをチェックし、認証成功時にビューを返します。
    """
    if test_func(request.user):  # ログイン済みの場合
        return view(request, *args, **kwargs)

    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == "basic":
            uname, passwd = base64.b64decode(auth[1]).decode().split(':')
            user = authenticate(username=uname, password=passwd)
            if user and user.is_active:
                login(request, user)
                request.user = user
                return view(request, *args, **kwargs)

    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = f'Basic realm="{realm}"'
    return response

def logged_in_or_basicauth(realm=""):
    """
    ログインまたはBasic認証でアクセスを許可するデコレーター。
    """
    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request, lambda u: u.is_authenticated, realm, *args, **kwargs)
        return wrapper
    return view_decorator

def has_perm_or_basicauth(perm, realm=""):
    """
    指定した権限があるユーザーにのみアクセスを許可するデコレーター。
    """
    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request, lambda u: u.has_perm(perm), realm, *args, **kwargs)
        return wrapper
    return view_decorator
