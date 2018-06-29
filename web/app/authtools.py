from django.http import HttpResponseNotFound, Http404, HttpResponseRedirect

def has_auth(func=None, redirect_url='/login'):
    def auth(request, *args, **kwargs):
        try:
            if not request.session["user"]:
                return HttpResponseRedirect(redirect_url + '?next=' + request.path)
        except KeyError:
            return HttpResponseRedirect(redirect_url + '?next=' + request.path)
        return func(request, *args, **kwargs)
    return auth
