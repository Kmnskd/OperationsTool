# !/bin/python3
import jenkins
import json


def create_jenkins_iob(data):
    # 登录jenkins
    server = jenkins.Jenkins(
        'http://xxx/jenkins/',
        username='xxx',
        password='xxxxxxxxx')
    server.build_job(
        "testFlightUpload",
        parameters={
            "baseline": json.dumps(data)})


def feature_temp_iob(data):
    # 登录jenkins
    server = jenkins.Jenkins(
        'http://xxx/jenkins/',
        username='xxx',
        password='xxxxxxx')
    server.build_job(
        "gitlab/test/feature_temp",
        parameters={
            "baseline": json.dumps(data)})