============
Installation
============

At the command line::

    $ pip install .

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv ciwatchenv
    $ pip install .


Configuration is stored in the ``ci-watch.conf`` file. Importantly, you can
specify a directory to store the ``third-party-ci.log`` file (data\_dir) as
well as the database to connect to. Look at ``ci-watch.conf.sample`` for an
example.

Other settings should be self explanatory based on the provided configuration
file.
