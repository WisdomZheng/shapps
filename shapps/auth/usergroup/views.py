# coding=utf-8
from uliweb import expose, functions, request, response, json, error, settings
from uliweb.i18n import ugettext_lazy as _
import json as json_
import os
import logging

log = logging.getLogger(__name__)


@expose('/usergroup')
class UserGroup(object):

    def __init__(self):
        self.UserGroupMd = functions.get_model("usergroup")


    def __begin__(self):
        functions.require_login()
        if not request.user.is_superuser:
            error(_('error: superuser role needed!'))


    def list(self):
        response.template = 'UserGroup/list.html'
        return{}


    def api_get_usergroupdata(self):
        if request.data:
            data = json_.loads(request.data)
        else:
            data = {}
        UserGroupMd = self.UserGroupMd
        sc_groupname = data.get("sc_groupname", "").strip()
        sc_grouptype = data.get("sc_grouptype", "").strip()
        sort = data.get("sort")
        order = data.get("order")
        limit = data.get("limit")
        offset = data.get("offset")

        grouplist = UserGroupMd.all()
        if sc_groupname:
            grouplist.filter(UserGroupMd.c.name.like('%%%s%%' % sc_groupname))
        if sc_grouptype == settings.USERGROUP.AUTHTYPE_LDAP:
            grouplist.filter(UserGroupMd.c.auth_type == settings.USERGROUP.AUTHTYPE_LDAP)
        elif sc_grouptype == settings.USERGROUP.AUTHTYPE_LOCAL:
            grouplist.filter(UserGroupMd.c.auth_type != settings.USERGROUP.AUTHTYPE_LDAP)

        if sort:
            sort_key = getattr(UserGroupMd.c, sort)
            if order:
                sort_key = getattr(sort_key, order)()
            grouplist.order_by(sort_key)
        if limit:
            grouplist.limit(limit)
        if offset:
            grouplist.offset(offset)

        return json({"total":grouplist.count(), "rows": [i.to_dict() for i in grouplist]})


    def view(self):
        from uliweb.utils.generic import DetailView
        group_id = int(request.values.get("id"))
        fields = [
            {'name':'name', 'verbose_name':_('GroupName')},
            {'name':'auth_type', 'verbose_name':_('AuthType')},
            {'name':'created_time', 'verbose_name':_('CreateTime')},
            {'name':'order', 'verbose_name':_('Order')},
            {'name':'deleted', 'verbose_name':_('Deleted')},
        ]
        obj = self.UserGroupMd.get(group_id)
        view = DetailView(self.UserGroupMd, obj=obj, fields=fields)
        response.template = 'UserGroup/view.html'
        return view.run()


    def add(self):
        response.template = 'UserGroup/add.html'
        errmsg = ""
        return {"errmsg":errmsg}


    def api_add(self):
        if request.data:
            data = json_.loads(request.data)
        else:
            data = {}
        data["name"] = data.get("name").strip()
        data["order"] = data.get("order").strip()
        data["auth_type"] = settings.USERGROUP.AUTHTYPE_LOCAL
        UserGroupMd = self.UserGroupMd
        if not data["groupname"]:
            return json({"msg":u"GroupName must be filled", "success":False})
        cnt = UserGroupMd.filter(UserGroupMd.c.name == data["groupname"]).count()
        if cnt > 0:
            return json({"msg":u"GroupName (%s) existed" % data["groupname"], "success":False})
        ret = UserGroupMd(**data).save()
        if ret:
            return json({"msg":u"Add GroupUser (%s) OK!" % data["groupname"], "success":True})
        else:
            return json({"msg":u"Fail to save UserGroup!", "success":False})


    def edit(self):
        response.template = 'UserGroup/edit.html'
        errmsg = ""
        UserGroupMd = self.UserGroupMd
        group_id = request.values.get("id")
        if group_id:
            userGroup = UserGroupMd.get(int(group_id))
        else:
            userGroup = None
        if not userGroup:
            errmsg = "UserGroup not found"
        return {"errmsg":errmsg, "userGroup":userGroup}

    def api_update(self):
        if request.data:
            data = json_.loads(request.data)
        else:
            data = {}
        data["name"] = data.get("name").strip()
        data["order"] = data.get("order").strip()
        data["auth_type"] = "local"
        UserGroupMd = self.UserGroupMd
        userGroup = UserGroupMd.get(int(data.get("id")))
        if not data["name"]:
            return json({"msg":u"GroupName must be filled", "success":False})
        cnt = UserGroupMd.filter(UserGroupMd.c.name == data["name"]).count()
        if userGroup.name != data["name"] and cnt > 0:
            return json({"msg":u"GroupName (%s) existed" % data["name"], "success":False})
        if userGroup.auth_type == settings.USERGROUP.AUTHTYPE_LDAP:
            return json({"msg":u"AuthTyppe(%s) does not allow to update" % userGroup.auth_type, "success":False})

        ret = userGroup.update(**data).save()
        if ret:
            return json({"msg":u"Update UserGroup (%s) OK!" % data["name"], "success":True})
        else:
            return json({"msg":u"Fail to update UserGroup!", "success":False})


    def api_remove(self):
        group_id = int(request.values.get("id"))
        UserGroupMd = self.UserGroupMd
        userGroup = UserGroupMd.get(group_id)
        cnt = userGroup.users.count()
        if cnt > 0:
            return json({"msg":u"The UserGroup has users.Please delete firstly", "success":False})
        if not userGroup:
            return json({"msg":u"This UserGroup  not found", "success":False})
        userGroup.delete()
        return json({"msg":u"Remove UserGroup (%s) OK!" % userGroup.name, "success":True})


    def adduser(self):
        User = functions.get_model('user')
        UserGroupMd = self.UserGroupMd

        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        user = User.get(int(user_id))
        userGroup = UserGroupMd.get(int(group_id))
        if not user:
            return json({'success':False, 'msg':"Can't find the user id %s" % user_id})
        if not userGroup:
            return json({'success':False, 'msg':"Can't find the UserGroup id %s" % userGroup})
        if userGroup.users.has(user):
            return json({'success':False, 'msg':"The user %s has already existed in UserGroup %s" % (user.username, userGroup.name)})
        else:
            userGroup.users.add(user)
            userdata = {'username':user.username, 'id':user.id}
            if hasattr(user, 'nickname'):
                userdata['nickname'] = user.nickname
            return json({'success':True, 'data':userdata, 'msg':"The user %s added to UserGroup(%s) successfully" % (user.username, userGroup.name)})


    def addbatchuser(self):
        User = functions.get_model('user')
        UserGroupMd = self.UserGroupMd

        user_ids = request.POST.get('user_ids')
        group_id = request.POST.get('group_id')
        user_ids = user_ids.replace('\n', ',').replace('\r', '').replace(u'，', ',')
        user_ids = user_ids.split(',')

        error_users = []
        for user_id in user_ids:
            if user_id != '':
                user = User.get(User.c.username == user_id)
                if not user:
                    error_users.append(user_id)

        if len(error_users) > 0:
            return json({'success':False, 'msg': u"下列人员帐号找不到： %s， 请仔细检查后再次增加。" % ','.join(error_users)})
        else:
            userGroup = UserGroupMd.get(int(group_id))
            for user_id in user_ids:
                user = User.get(User.c.username == user_id)
                if not userGroup.users.has(user):
                    userGroup.users.add(user)
            msg = "批量增加人员成功"
            # flash(msg, category='success')
            return json({'success':True, 'msg': msg});


    def deluser(self):
        User = functions.get_model('user')
        UserGroupMd = self.UserGroupMd

        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        user = User.get(int(user_id))
        userGroup = UserGroupMd.get(int(group_id))
        if not user:
            return json({'success':False, 'msg':"Can't find the user id %s" % user_id})
        if not userGroup:
            return json({'success':False, 'msg':"Can't find the UserGroup id %s" % group_id})
        if userGroup.auth_type == settings.USERGROUP.AUTHTYPE_LDAP:
            return json({'success':False, 'msg':"The 'ldap' UserGroup does not allow to del.id is %s" % group_id})

        if userGroup.users.has(user):
            userGroup.users.remove(user)
            return json({'success':True, 'msg':"The user %s has been delete from UserGroup(%s) successfully." % (user.username, userGroup.name)})
        else:
            return json({'success':False, 'msg':"The user %s is not existed in UserGroup %s ." % (user.username, userGroup.name)})

