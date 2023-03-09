# !/bin/python3

from flask import Blueprint
from flask import request, make_response, render_template
from utils.jenkins_job import feature_temp_iob
import time

feature = Blueprint("feature", __name__)

environment_info = {"feature": 3, "dev": 2}


@feature.route("/feature_deploy", methods=["GET", "POST"])
def upload_package():
    if request.method == "POST":
        data = request.values.to_dict()
        environment = data.get("environment")
        random_num = str(time.time()).split(".")[0]
        tag = "100.100.100.%s.%s" % (environment_info.get(environment, None), random_num)
        if environment == "prd":
            tag = "100.100.%s" % random_num
        data["tag"] = tag
        data["task_name"] = "feature"
        if environment.__contains__("ack"):
            data["ack"] = "true"
            data["environment"] = environment.split("_")[-1]
        feature_temp_iob(data)
        response = make_response('success upload', 200)
        return response
    else:
        return render_template("featureDeploy.html")
