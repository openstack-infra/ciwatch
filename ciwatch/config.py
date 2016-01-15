# Copyright (c) 2015 Tintri. All rights reserved.
# Copyright (c) 2016 IBM Corporation
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
from six.moves.configparser import ConfigParser


class CanNotReadConfigException(Exception):
    pass


class ConfigOptionMissingException(Exception):
    pass


class Config(object):

    def __init__(self, locations=['/etc/ciwatch/ciwatch.conf',
                                  '~/.ciwatch.conf']):
        self.cfg = ConfigParser()
        self._set_defaults()
        self._read(locations)

    def _set_defaults(self):
        self._set_default('AccountInfo', 'gerrit_host', 'review.openstack.org')
        self._set_default('AccountInfo', 'gerrit_port', 29418)
        self._set_default('Data', 'data_dir', '/var/lib/ciwatch')
        self._set_default('Log', 'log_dir', '/var/log/ciwatch')
        self._set_default('database', 'connection', 'sqlite://')
        self._set_default('misc', 'projects', ','.join([
            'cinder',
            'devstack',
            'ironic',
            'manila'
            'murano',
            'neutron',
            'neutron-lbaas',
            'nova',
            'octavia',
            'os-brick',
            'rally',
            'swift',
        ]))

    def _read(self, locations):
        if not isinstance(locations, list):
            locations = [locations]
        locations = [os.path.expanduser(x) for x in locations]

        files_loaded = self.cfg.read(locations)
        if files_loaded == []:
            raise CanNotReadConfigException('Locations tried: %s' % locations)
        # TODO(mmedvede): log.debug('Read config from %s' % files_loaded)

    def _set_default(self, section, option, value):
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        if not self.cfg.has_option(section, option):
            self.cfg.set(section, option, value)

    # ConfigParser in Python 3 provides fallback form for free. Implement our
    # own for Python 2.7.
    def get(self, section, option, fallback=None):
        if (self.cfg.has_section(section) and
                self.cfg.has_option(section, option)):
            return self.cfg.get(section, option)
        elif fallback is not None:
            return fallback
        else:
            raise ConfigOptionMissingException('%s.%s' % (section, option))
