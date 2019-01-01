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


How it works
-------------
A FeedbackForm contains one or more FormElement models of different ElementType.
The data is collected for each submission into FeedbackData.

A REST Api is exposed to allow manipulating the models externally, which is useful when this is deployed
into a backend service.

In addition, a view to accept form submissions is provided, as well as template tags to render a complete form
or part of it.
