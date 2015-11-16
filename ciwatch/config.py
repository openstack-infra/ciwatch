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

import os

from iniparse import INIConfig


class Config(object):

    def __init__(self):
        self.cfg = self.get_config()
        if self.cfg.Data.data_dir:
            self.DATA_DIR = self.cfg.Data.data_dir
        else:
            self.DATA_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))) + '/data'

    def get_config(self):
        this_file = os.path.dirname(os.path.realpath(__file__))
        this_dir = os.path.dirname(this_file)
        conf_files = [os.path.join(this_dir, 'ciwatch.conf'),
                      '/etc/ciwatch/ciwatch.conf']
        # Read first existing conf file, ignore the rest
        for conf_file in conf_files:
            if os.path.exists(conf_file):
                return INIConfig(open(conf_file))
        else:
            raise Exception(
                'Could not read configuration from %s' % conf_files)

    def get_projects(self):
        projects = []
        for name in self.cfg.misc.projects.split(','):
            projects.append(name)
        return projects
