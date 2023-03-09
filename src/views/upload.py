# !/bin/python3

from datetime import datetime
from flask import Blueprint
from flask import request, make_response, render_template
from utils.jenkins_job import create_jenkins_iob

upload = Blueprint("upload", __name__)


@upload.route("/upload_package", methods=["GET", "POST"])
def upload_package():
    if request.method == "POST":
        data = request.values.to_dict()
        update_time = datetime.now().strftime("%Y--%m--%d %H:%M:%S")
        package_url = data.get("package_url")
        package_name = package_url.split("/")[-1]
        data["package_name"] = package_name
        data["update_time"] = update_time
        data["task_name"] = "ios"
        create_jenkins_iob(data)
        response = make_response('success upload', 200)
        return response
    else:
        return render_template("iosTestFlight.html")
