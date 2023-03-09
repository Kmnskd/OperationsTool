#!/usr/bin/env python3
# -*- coding:utf-8  -*-

import requests

baselic_service = [
    "baselic-frontend",
    "baselic-auth",
    "baselic-project",
    "baselic-version",
    "devp-client-integration",
    "devp-user-center",
    "devp-api-gateway",
    "baselic-board",
    "baselic-build",
]


def get_version_info(current_env):
    version_info = {}
    cloud_tag = get_tags(current_env, "devp-user-center")
    frontend_tag = get_tags(current_env, "baselic-frontend")
    version_info["cloud_tag"] = cloud_tag
    version_info["frontend_tag"] = frontend_tag
    return version_info


def get_tags(current_env, separation):
    headers = {"Content-Type": "application/json"}
    get_url = "http://xxx.xxx.xxx.xxx:8081/api/v2.0/projects/%s/repositories/%s/artifacts" \
        "?with_tag=true&with_scan_overview=true&with_label=true&page_size=15&page=1" % (current_env, separation)
    res = requests.get(headers=headers, url=get_url, verify=False)
    data = res.json()
    tag = []
    for i in data:
        tag_name = [name.get("name") for name in i.get("tags")]
        tag.append(tag_name[0])
    return tag
