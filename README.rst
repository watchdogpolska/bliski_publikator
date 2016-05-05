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

Running tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pip install -r requirements/test.txt
  $ python manage.py tests


Running tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard develop server::

  $ pip install -r requirements/local.txt
  $ python manage.py migrate
  $ python manage.py runserver

SQL-logging develop server::

  $ SQL_LOG=True python manage.py runserver

Frontend build
^^^^^^^^^^^^^^

In development
    $ npm install
    $ gulp

In production
    $ npm install
    $ gulp prod

Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at http://getsentry.com or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

It's time to write the code!!!

## Gulp

Gulp is a task runner used for automatic style/script compilation, minification, Angular app compilation; etc.

### Defined task:
* default - Run task `dev`, so build app, run server, proxy and begins to watch files
  ````
  gulp
  ````
* **prod** - run task ``bower``, ``delete:prod``, ``script``, ``styles``, ``optimzie``, ``inject``, ``webpack``.
When you run this command, the application is ready to make publicly available. All files will be ready.
* *build* - Build app for development.
* bower - run ```bower install```. It download frontend depedencies (TinyMce, Bootstrap, Font-awesome...)-
  ````
  gulp bower
  ````
* browsersync - Run proxy server. It's a developer tools used for livereloading, scroll synchronization and other. Read more: https://www.browsersync.io/
  ````
  gulp browsersync
  ````
* delete - Deletes static files created when building applications. Does delete compiled angular 2 app.
* delete:prod - Delete also production template with injected script/styles (see ``inject``).
* inject - injects project, django apps and third party dependencies in the base template
* dev - see ``defualt``
* fonts - copy fonts files from bower
* optimize - minify/concat css/js for production
* script - transpile script from assets to static.
* styles - compile scss to css.
* watch - Start watching for changes in styles, script. See ````script````, ````styles````.

Summary:\
Do you want to prepare applications for production? ``gulp prod``\
Do you want to start programming ? Just ``gulp``\
Do you only want to build applications without observing changes for developming? ``gulp build``
