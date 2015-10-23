========
CI Watch
========

CI Watch is a CI monitoring dashboard that shows voting history for existing
CIs and more.

* Free software: Apache license
* Documentation: http://docs.openstack.org/infra/ciwatch
* Source: http://git.openstack.org/cgit/openstack-infra/ciwatch
* Bugs: http://bugs.launchpad.net/ciwatch


State of the project
--------------------

This project is a work in progress and the code is pretty rough in some
places.

TODO
----

-  Add tests.
-  Use a different cache other than SimpleCache. It is not threadsafe.
   We should use something like redis instead.

These items are far from the only work needed for this project.

Acknowledgements
----------------

This code was originally forked from John Griffith's sos-ci project.
Some of it can still be found in the code and configuration file.
