from datetime import datetime
from flask import Blueprint, jsonify
from flask import request, make_response, render_template, redirect, url_for
from utils.jenkins_job import create_jenkins_iob
from utils.image_roback import get_version_info
from flask import session

rollout = Blueprint("rollout", __name__)


@rollout.before_request
def before_request():
    if request.path == "/static/login.html" or request.path == "/auth/login" or request.path.endswith(".js") or request.path.endswith(".css"):
        pass
    else:
        username = session.get('username')
        if not username:
            return redirect('/static/login.html')


@rollout.route("/version_rollout", methods=["GET", "POST"])
def version_rollout():
    if request.method == "POST":
        data = request.values.to_dict()
        data["task_name"] = "zone"
        if data.get("cloud_version") == "0" and data.get("frontend_version") == "0":
            return render_template("versionRollout.html")
        create_jenkins_iob(data)
        return render_template("versionRollout.html")
    else:
        return render_template("versionRollout.html")


@rollout.route("/image_version", methods=["POST"])
def get_image_version():
    if request.method == "POST":
        data = request.values.to_dict()
        environment = "baseline-" + data.get("environment", "dev")
        version_info = get_version_info(environment)
        return {"version_info": version_info}
