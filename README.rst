========================
django-connect
========================

A project template to jumpstart large projects with Facebook Connect, Heroku, Amazon S3, and more.

Working Environment
===================

You have several options in setting up your working environment.  We recommend
using virtualenv to separate the dependencies of your project from your system's
python environment.  If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

Virtualenv with virtualenvwrapper
------------------------------------

You need virtualenv with virtualenvwrapper for quick setup::

    $ mkvirtualenv django_connect
    
To activate virtualenv::

    $ workon django_connect


Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt
    
    
Sync Database
=============================

Depending on where you are installing dependencies:

In development::

    $ python manage.py syncdb --settings=django_connect.settings.local

For production::

    $ python manage.py syncdb --settings=django_connect.settings.local


Runserver
=============================

Depending on where you are installing dependencies:

In development::

    $ python manage.py runserver --settings=django_connect.settings.local

For production::

    $ python manage.py runserver --settings=django_connect.settings.local
    

Acknowledgements
================

- Many thanks to Two Scoops of Django authors Daniel Greenfeld, Audrey M. Roy, and everyone else who has contributed.
