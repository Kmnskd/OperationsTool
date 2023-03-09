from flask import Blueprint
from flask import request, render_template, redirect
from utils.conn_ldap import LdapManager
from flask import session

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['get', 'post'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    res, code = LdapManager().check_auth(username, password)
    if res:
        session['username'] = username
        return redirect("/rollout/version_rollout")
    else:
        content = {"res": res, "code": code}
        return render_template("error.html", content=content)


@auth.route("/logout")
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/')
