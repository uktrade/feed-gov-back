=====
Feed Gov Back
=====

A small API enabled framework for adding user feedback forms to existing applications within GOV.uk (or other apps).


Quick start
-----------

1. Install the package::

    pip install feed-gov-back


2. Add `feedback` to your `INSTALLED_APPS` in your `settings`::

    INSTALLED_APPS = [
        ...
        'feedback',
    ]

3. Include the feedback URLconf in your project urls.py like this::

    path('feedback/', include('feedback.services.urls'))

4. Run migrations and load fixtures::

    ./manage.py migrate
    ./manage.py loaddata path/to/fedback/fixtures/*.json
