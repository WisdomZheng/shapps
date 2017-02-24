# introduction

uliweb app for user login with verification code

# api example
you should set auth type in settings if you want to use specific type. (Default=None)
use type ldap for example:
you can use shapps.auth.ldap directly or overwrite settings.ini about section [AUTH] and [AUTH_CONFIG]

then add this app in settings.ini:
```
[GLOBAL]
INSTALLED_APPS = [
    ...
    'shapps.auth.verification_code',
    ...
]
```