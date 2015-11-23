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

from datetime import datetime
import json
import re

from ciwatch.config import Config
from ciwatch import db
from ciwatch.log import logger
from ciwatch import models
from zuul.lib.gerrit import Gerrit


def _process_project_name(project_name):
    return project_name.split('/')[-1]


def _process_event(event):
    comment = event['comment']
    # Find all the CIs voting in this comment
    lines = comment.splitlines()
    event['ci-status'] = {}
    for line in lines:
        possible_results = "FAILURE|SUCCESS|NOT_REGISTERED|UNSTABLE"
        pattern = re.compile("[-*]\s+([^\s*]+)\s+(http[^\s*]+) : (%s)" %
                             possible_results)
        match = pattern.search(line)
        if match is not None:
            ci_name = match.group(1)
            log_url = match.group(2)
            result = match.group(3)
            event['ci-status'][ci_name] = {
                "result": result,
                "log_url": log_url}


def _is_ci_user(name):
    return 'CI' in name or 'Jenkins' in name or 'Bot' in name


# Check if this is a third party CI event
def _is_valid(event, projects):
    if (event.get('type', 'nill') == 'comment-added' and
            _is_ci_user(event['author'].get('name', '')) and
            _process_project_name(
                event['change']['project']) in projects and
            event['change']['branch'] == 'master'):
        return True
    return False


def _store_event(event, datadir):
    with open(datadir + '/third-party-ci.log', 'a') as f:
        json.dump(event, f)
        f.write('\n')
    add_event_to_db(event)
    return event


def parse_event(event, projects):
    if _is_valid(event, projects):
        _process_event(event)
        logger.info('Parsed valid event: %s', event)
        return event
    return None


def add_event_to_db(event, commit_=True):
    session = db.Session()
    project = session.query(models.Project).filter(
        models.Project.name == _process_project_name(
            event["change"]["project"])).one()
    patch_set = db.get_or_create(
        models.PatchSet,
        commit_=False,
        project_id=project.id,
        ref=event['patchSet']['ref'],
        commit_message=event['change']['commitMessage'],
        created=datetime.fromtimestamp(
            int(event['patchSet']['createdOn'])))

    owner_name = event["author"]["name"]
    owner = db.get_or_create(models.CiOwner, name=owner_name)
    trusted = (event["author"]["username"] == "jenkins")

    if trusted and "approvals" in event:
        if event["approvals"][0]["value"] in ("1", "2"):
            patch_set.verified = True
        elif event["approvals"][0]["value"] in ("-1", "-2"):
            patch_set.verified = False

    for ci, data in event['ci-status'].iteritems():
        ci_server = db.get_or_create(models.CiServer,
                                     commit_=False,
                                     name=ci,
                                     trusted=trusted,
                                     ci_owner_id=owner.id)
        db.update_or_create_comment(commit_=False,
                                    result=data["result"],
                                    log_url=data["log_url"],
                                    ci_server_id=ci_server.id,
                                    patch_set_id=patch_set.id)
    if commit_:
        session.commit()


def main():
    config = Config()
    db.create_projects()  # This will make sure the database has projects in it
    gerrit = Gerrit(
        hostname=config.cfg.AccountInfo.gerrit_host,
        username=config.cfg.AccountInfo.gerrit_username,
        port=int(config.cfg.AccountInfo.gerrit_port),
        keyfile=config.cfg.AccountInfo.gerrit_ssh_key
    )
    gerrit.startWatching()
    while True:
        event = gerrit.getEvent()[1]
        parsed_event = parse_event(event, config.get_projects())
        if parsed_event is not None:
            _store_event(parsed_event, config.DATA_DIR)

if __name__ == '__main__':
    main()
