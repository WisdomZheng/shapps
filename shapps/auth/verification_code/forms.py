#coding=utf-8
from uliweb import functions, settings
from uliweb.form import *
from uliweb.i18n import ugettext as _
from uliweb.core.html import Tag
from uliweb.form.widgets import Build
from uliweb.form import BaseField, UnicodeField

class Image(Build):
    '''
       create new Build, use for verification code image display
    '''
    def to_html(self):
        args = self.kwargs.copy()
        value = args.pop('value', None)
        return str(Tag('img', value, **args)) + "<span id='refresh' class='glyphicon glyphicon-refresh icon-refresh'></span>"

class VerificationCodeInputField(UnicodeField):
    '''
       extend UnicodeField for verification code checking
    '''
    def validate(self, data, all_data=None):
        username = all_data.get("username")
        if not data:
            return False, "This field is required."
        else:
            login_failed_history = functions.get_model("login_failed_history")
            login_failed_user = login_failed_history.get(login_failed_history.c.username == username)
            if login_failed_user:
                if data.lower() != login_failed_user.verification_code.lower():
                    return False, "verification code does not match"
            return True, data

class VerificationCodeField(BaseField):
    '''
       create new Field for verification code display
    '''
    default_build = Image
    type_name = 'img'

    def __init__(self, label='', default='', required=False, validators=None, name='', html_attrs=None, help_string='', build=None, **kwargs):
        BaseField.__init__(self, label=label, default=default, required=required, validators=validators, name=name, html_attrs=html_attrs, help_string=help_string, build=build, **kwargs)

class CheckLoginForm(Form):
    '''
       form for use verification code
    '''
    form_buttons = Submit(value=_('Login'), _class="btn btn-primary")

    username = UnicodeField(label=_('Username'), required=True)
    password = PasswordField(label=_('Password'), required=True)
    verification_code = VerificationCodeInputField(label=_('Verification Code'), required=True)
    verification_img = VerificationCodeField()
    rememberme = BooleanField(label=_('Remember Me'))
    next = HiddenField()