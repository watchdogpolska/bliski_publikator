.. image:: https://codecov.io/github/watchdogpolska/bliski_publikator/coverage.svg?branch=master
    :target: https://codecov.io/github/watchdogpolska/bliski_publikator?branch=master
    :alt: Coverage Status

.. image:: https://travis-ci.org/watchdogpolska/bliski_publikator.svg?branch=master
    :target: https://travis-ci.org/watchdogpolska/bliski_publikator
    :alt: Build Status

.. image:: https://requires.io/github/watchdogpolska/bliski_publikator/requirements.svg?branch=master
     :target: https://requires.io/github/watchdogpolska/bliski_publikator/requirements/?branch=master
     :alt: Requirements Status

bliski_publikator
==============================

Celem strony jest pokazanie, jakie informacje są w posiadaniu spółek, a mimo to nie publikują one ich na BIP + wskazanie, czemu te informacje są czy mogą być ważne dla mieszkańców i zachęcenie mieszkańców do interesowania się.


LICENSE: BSD

Settings
------------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.org/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you’d like to take advantage of live reloading and Sass / JS compilation you can do so with a little bit of prep work.

Make sure that nodejs, gulp-cli, bower is installed. Then in the project root run:

    $ npm install

Now you just need:

    $ gulp watch

The base app will now run as it would with the usual manage.py runserver but with live reloading and Sass compilation enabled.

To get live reloading to work you won't need to install an appropriate browser extension.  It's provided by proxying request and injecting script.


Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at http://getsentry.com or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

It's time to write the code!!!
