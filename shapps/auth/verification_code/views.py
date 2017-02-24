#coding=utf-8

from forms import *
from uliweb.form import *
from uliweb import expose, settings, request, functions
from uliweb.contrib.auth.forms import LoginForm
from uliweb.contrib.auth.views import add_prefix
from uliweb.core.SimpleFrame import redirect
from uliweb.i18n import ugettext as _
from . import gene_code
import urllib
import logging

logger = logging.getLogger('verification_code_login')

def login():
    from uliweb.contrib.auth import login

    text = ""
    username = request.params.get("username", "")

    form = LoginForm()

    if request.user:
        next = request.GET.get('next')
        if next:
            return redirect(next)

    if request.method == 'GET':
        form.next.data = request.GET.get('next', request.referrer or add_prefix('/'))
        return {'form':form, 'msg':'', 'username': username}
    if request.method == 'POST':
        login_failed_history = functions.get_model("login_failed_history")
        login_failed_user = login_failed_history.get(login_failed_history.c.username == username)

        if login_failed_user and login_failed_user.failed_times >= settings.VERIFICATIONCODE.FAILED_TIMES:
            form = CheckLoginForm()

        flag = form.validate(request.params)
        try:
            if flag:
                if not login_failed_user:
                    login_failed_user = login_failed_history(username = username, failed_times = 0, verification_code = text)
                    login_failed_user.save()

                f, d = functions.authenticate(username = form.username.data, password = form.password.data)
                if f:
                    request.session.remember = form.rememberme.data
                    login(form.username.data)
                    login_failed_user.update(failed_times = 0).save()
                    next = urllib.unquote(request.POST.get('next', add_prefix('/')))
                    return redirect(next)
                form.errors.update(d)
                current_failed_times = login_failed_user.failed_times
                current_failed_times = current_failed_times + 1
                if current_failed_times >= settings.VERIFICATIONCODE.FAILED_TIMES:
                    text = gene_code(username)
                    if not isinstance(form, CheckLoginForm):
                        form = CheckLoginForm()
                login_failed_user.update(failed_times = current_failed_times, verification_code = text).save()
            else:
                if login_failed_user and login_failed_user.failed_times >= settings.VERIFICATIONCODE.FAILED_TIMES:
                    text = gene_code(username)
                    login_failed_user.update(verification_code = text).save()
        except Exception, e:
            logger.error("count user: [%s] login failed times error" % (username))
            logger.error("-- error message: %s" % (e))
        msg = form.errors.get('_', '') or _('Login failed!')
        return {'form':form, 'msg':str(msg), 'username': username}

@expose('/api/refreshcode')
def refresh_code():
    username = request.params.get("username", "")
    text = gene_code(username)
    login_failed_history = functions.get_model("login_failed_history")
    login_failed_user = login_failed_history.get(login_failed_history.c.username == username)
    if login_failed_user and login_failed_user.failed_times >= settings.VERIFICATIONCODE.FAILED_TIMES:
        try:
            login_failed_user.update(verification_code = text).save()
        except Exception, e:
            logger.error("store refreshed verification code for user: [%s] failed" % (username))
            logger.error("-- error message: %s" % (e))
        return json({"result": "success"})
    else:
        return json({"result": "failed", "message": "refresh verification code failed"})