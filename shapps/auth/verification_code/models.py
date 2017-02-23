#! /usr/bin/env python
#coding=utf-8

from uliweb.orm import *

class LoginFailedHistory(Model):
    """
       count times for user when login failed
    """
    username = Field(str, verbose_name = "username", max_length = 64)
    failed_times = Field(int, verbose_name = "failed_times")
    verification_code = Field(str, verbose_name = "verification_code", max_length = 8)