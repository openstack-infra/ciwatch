# Copyright (c) 2016 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.  You may obtain a
# copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ciwatch.config import Config
from ciwatch.tests import base
from testtools import ExpectedException
from testtools.matchers import Equals

from ciwatch.config import CanNotReadConfigException
from ciwatch.config import ConfigOptionMissingException


class TestConfiguration(base.TestCase):

    def test_config_file_does_not_exist(self):
        bad_path = '/etc/non/existing'
        self.can_not_read_config_at(bad_path)
        self.can_not_read_config_at([bad_path])
        self.can_not_read_config_at([bad_path, bad_path])

    def can_not_read_config_at(self, path):
        with ExpectedException(CanNotReadConfigException):
            Config(path)

    def test_config_file_exists(self):
        [good_path] = self.create_tempfiles([('emptyfile', '')])
        self.can_read_config_at(good_path)
        self.can_read_config_at([good_path])
        self.can_read_config_at([good_path, good_path])

    def can_read_config_at(self, path):
        Config(path)

    def test_get(self):
        [empty_config] = self.create_tempfiles([('empty_config', '')])
        self.config = Config(empty_config)

        self.missing_option_raises_exception()
        self.get_fallback_works_for(25)
        self.get_fallback_works_for(True)
        self.get_fallback_works_for('DummyValue')

    def missing_option_raises_exception(self):
        with ExpectedException(ConfigOptionMissingException):
            self.config.get('missing_section', 'missing_option')

    def get_fallback_works_for(self, fallback_value):
        fallback = self.config.get(
            'section', 'missing_option', fallback_value)
        self.assertThat(fallback, Equals(fallback_value))

    def test_set_default(self):
        [empty_config] = self.create_tempfiles([('empty_config', '')])
        self.config = Config(empty_config)

        with ExpectedException(ConfigOptionMissingException):
            self.config.get('section', 'option')

        self.config._set_default('section', 'option', 'value')
        value = self.config.get('section', 'option')
        self.assertThat(value, Equals('value'))
