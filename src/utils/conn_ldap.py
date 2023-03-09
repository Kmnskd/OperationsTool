import re
import random
import string

from ldap3 import Connection, Server, ALL, core, SUBTREE
from ldap3.core.exceptions import LDAPBindError
from ldap3.extend.standard.modifyPassword import ModifyPassword

from utils.errors import LdapManagerError
from utils.mail import send_mail


class LdapManager(object):
    def __init__(self):
        self.user = "xxx"
        self.password = ["xxx"]

    def connect(self, username=None, password=None):
        server = Server('xxx.xxx.xxx.xxx', get_info=ALL)
        if username and password:
            self.user = 'uid={},ou=users,dc=xxx,dc=xxx'.format(username)
            self.password = password
        conn = Connection(server, self.user, self.password, auto_bind=True)
        return conn

    def check_auth(self, username, password):
        if username not in self.admin_list:
            return False, 1
        try:
            self.connect(username, password)
        except core.exceptions.LDAPBindError:
            return False, 2
        return True, 0

    def create_user(self, data):
        conn = self.connect()
        object_class = ["posixAccount", "top", "inetOrgPerson"]
        uid_new, attributes_user = self.create_user_info(data)
        conn.search(search_base='ou=users,dc=xxx,dc=xxx',
                    search_filter='(objectClass=inetOrgPerson)',
                    search_scope=SUBTREE,
                    attributes=['uid', 'employeeNumber', 'telephonenumber'])
        user_info = conn.response
        # 判断工号唯一，电话号唯一
        uid_list = []
        for i in user_info:
            attributes_all = i.get('attributes')
            employeeNumber_old = attributes_all.get('employeeNumber')
            uid_old = attributes_all.get('uid')[0]
            telephonenumber_old = attributes_all.get('telephonenumber')

            if employeeNumber_old == attributes_user.get("employeeNumber") or \
                telephonenumber_old == attributes_user.get("telephonenumber"):
                raise LdapManagerError("user already exist.")

            if uid_old == uid_new:
                uid_list.append(0)

            if re.search("%s[0-9]" % str(uid_new), str(uid_old)):
                uid_list.append(int(uid_old.split(uid_new)[-1]))
        if uid_list:
            uid_new = uid_new + str(max(uid_list)+1)

        attributes_user["homeDirectory"] = "/home/users/" + uid_new

        try:
            conn.add("uid=%s,ou=users,dc=xxx,dc=xxx" % uid_new, object_class=object_class, attributes=attributes_user)
            status = conn.result.get("description")
            # print(conn.result)
            conn.unbind()
        except Exception as e:
            raise LdapManagerError(str(e))
        if status == "success":
            mail = attributes_user.get("mail")
            cn = attributes_user.get("cn")
            send_mail("register", mail, cn, uid_new)
        return status

    def create_user_info(self, data):
        uid = data.get("uid")
        cn = displayName = data.get("cn")
        mail = data.get("mail")
        employeeNumber = data.get("employeeNumber")
        uidnumber = self.deal_uidnumber(employeeNumber)
        telephonenumber = data.get("telephonenumber")
        homeDirectory = ""
        userPassword = "xxxx"
        gidnumber = 0
        sn = cn[0]
        givenname = cn[1:]
        attributes = {"cn": cn, "displayName": displayName, "mail":  mail,
                      "gidnumber": gidnumber, "employeeNumber": employeeNumber, "givenname": givenname,
                      "homeDirectory": homeDirectory, "userPassword": userPassword,
                      "sn": sn, "uidnumber": uidnumber, "telephonenumber": telephonenumber}
        return uid, attributes

    @staticmethod
    def deal_uidnumber(employeeNumber):
        # 删除工号前面的所有字母，只留下数据
        for i in employeeNumber:
            try:
                int(i)
            except ValueError:
                employeeNumber = employeeNumber.split(i)[-1]
        # 删除工号前面的0，只留下数据
        for j in employeeNumber:
            if int(j) > 0:
                return employeeNumber
            else:
                employeeNumber = employeeNumber[employeeNumber.index(j)+1:]

    def update_passwd(self, data, reset=False):
        user = None
        current_passwd = None
        username = data.get("username")
        if not username:
            raise LdapManagerError("用户名或密码错误")
        if reset:
            # 重置密码
            new_passwd = ''.join(random.sample(string.ascii_letters + string.digits, 12))
            user = "uid={},ou=users,dc=xxx,dc=xxx".format(username)
        else:
            current_passwd, new_passwd = self.passwd_complex(data)
        try:
            con = self.connect(username, current_passwd)
            modify = ModifyPassword(con, user=user, new_password=new_passwd)
            resp = modify.send()
            message = modify.result.get("message")
        except LDAPBindError:
            raise LdapManagerError("用户名或密码错误")
        # 重置发邮件
        if resp and reset:
            user_info = self.get_user_attributes(user, ['mail'])
            for i in user_info:
                attributes_all = i.get('attributes')
                mail = attributes_all.get("mail")[0]
            send_mail("reset", mail, username, new_passwd)
            message = "密码重置成功，密码已发送您的邮箱（%s）！" % mail
        return resp, message

    def passwd_complex(self, data):
        current_passwd = data.get("current_passwd")
        new_passwd = data.get("new_passwd")
        new_passwd_again = data.get("new_passwd_again")
        if new_passwd != new_passwd_again:
            raise LdapManagerError("两次密码输入不一致")
        if len(new_passwd) < 8 or len(new_passwd) > 20:
            raise LdapManagerError("密码必须大于8位和小于20位")
        if not re.match(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[!@#$%^~&*()\-_=+{};:<,.>?\[\]])[a-zA-Z\d!@#$%^~&*()\-_=+{};:<,.>?\[\]]*$', new_passwd):
            raise LdapManagerError("密码至少包含一个大小写字母和特殊字符")

        return current_passwd, new_passwd

    def get_user_attributes(self, ou, attributes):
        con = self.connect()
        con.search(search_base=ou,
                   search_filter='(objectClass=inetOrgPerson)',
                   search_scope=SUBTREE,
                   attributes=attributes)
        return con.response
