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

import json
import os

from ciwatch.config import Config
from ciwatch import db
from ciwatch.events import add_event_to_db
from ciwatch.events import parse_event
from ciwatch.log import logger


def get_data(datafile, projects):
    data = []
    with open(datafile) as file_:
        for line in file_:
            try:
                event = json.loads(line)
            except Exception as ex:
                logger.error('Failed json.loads on event: %s', event)
                logger.exception(ex)
                continue
            parsed_event = parse_event(event, projects)
            if parsed_event is not None:
                data.append(parsed_event)
    return data


def load_data(data):
    for event in data:
        add_event_to_db(event, commit_=False)
    db.Session().commit()


def main():
    config = Config()
    projects = config.get('misc', 'projects').split(',')
    datadir = config.get('Data', 'data_dir')
    datafile = os.path.join(datadir, 'third-party-ci.log')
    db.create_projects(projects)
    data = get_data(datafile, projects)
    load_data(data)


if __name__ == '__main__':
    main()
