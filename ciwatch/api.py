# Copyright (c) 2015 Tintri. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from collections import OrderedDict
from datetime import datetime
from datetime import timedelta

from flask import request

from ciwatch import db

TIME_OPTIONS = OrderedDict([  # Map time options to hours
    ("24 hours", 24),
    ("48 hours", 48),
    ("7 days", 7 * 24),
])

DEFAULT_TIME_OPTION = "24 hours"
DEFAULT_PROJECT = "cinder"


def _get_ci_info_for_patch_sets(ci, patch_sets):
    ci_info = {"name": ci.name, "trusted": ci.trusted, "results": []}
    for patch_set in patch_sets:
        for comment in patch_set.comments:
            if comment.ci_server_id == ci.id:
                ci_info["results"].append(comment)
                break
        else:  # nobreak
            ci_info["results"].append(None)
    return ci_info


def get_time_options():
    return TIME_OPTIONS.keys()


def get_context():
    project_name = request.args.get('project', DEFAULT_PROJECT)
    time = request.args.get('time', DEFAULT_TIME_OPTION)
    since = datetime.now() - timedelta(hours=TIME_OPTIONS[time])
    project = db.get_project(project_name)
    patch_sets = db.get_patch_sets(project, since)
    results = OrderedDict()
    for ci in db.get_ci_servers():
        ci_info = _get_ci_info_for_patch_sets(ci, patch_sets)
        if any(result for result in ci_info["results"]):
            results[ci.ci_owner] = results.get(ci.ci_owner, [])
            results[ci.ci_owner].append(
                _get_ci_info_for_patch_sets(ci, patch_sets))

    return {"time_options": get_time_options(),
            "time_option": time,
            "patch_sets": patch_sets,
            "project": project,
            "projects": db.get_projects(),
            "user_results": results}
