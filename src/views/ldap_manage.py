from flask import Blueprint
from flask import request, make_response, render_template, jsonify, request, redirect
from flask_json_schema import JsonSchema, JsonValidationError
from utils.conn_ldap import LdapManager, LdapManagerError
from ldap3.core.exceptions import LDAPBindError
from schema.json_schema import ldap_schema
from flask_expects_json import expects_json
import json
from utils.errors import ErrorStatus


ldap_manage = Blueprint("ldap_manage", __name__)
error = ErrorStatus()


@ldap_manage.route("/create_user", methods=["POST"])
# @expects_json(ldap_schema)
def ldap_create_user():
    form_status = request.json.get("status")
    if form_status != "DONE":
        return error.status_code(400, "failed", "Created user failed")
    try:
        data = json.loads(request.json.get("form_data"))
        status = LdapManager().create_user(data)
    except LdapManagerError as e:
        return error.status_code(400, "failed", str(e))
    except Exception as e:
        return error.status_code(400, "failed", str(e))
    if status == "success":
        return error.status_code(200, "success", 'Created user succeed')


@ldap_manage.route("/update_passwd", methods=["GET", "POST"])
def update_passwd():
    if request.method == "POST":
        # print(request.json)
        data = request.values.to_dict()
        username = data.get("username")
        current_passwd = data.get("current_passwd")
        new_passwd = data.get("new_passwd")
        new_passwd_again = data.get("new_passwd_again")
        print(username, current_passwd, new_passwd, new_passwd_again)
        try:
            resp, message = LdapManager().update_passwd(data)
        except LDAPBindError as e:
            return error.status_code(401, "failed", str(e))
        except LdapManagerError as e:
            return error.status_code(401, "failed", str(e))
        if not resp:
            return error.status_code(403, "failed", message)
        return error.status_code(200, "success", "密码修改成功")

    return render_template("updatePasswd.html")


@ldap_manage.route("/reset_passwd", methods=["GET", "POST"])
def reset_passwd():
    if request.method == "POST":
        data = request.values.to_dict()
        print(data)
        resp, message = LdapManager().update_passwd(data, reset=True)
        if not resp:
            return error.status_code(401, "failed", "用户名不存在！")
        return error.status_code(200, "success", message)
    return render_template("updatePasswd.html")