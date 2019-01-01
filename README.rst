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

    or if not using the Api:

    path('feedback/', include('feedback.urls'))

4. Run migrations and load fixtures::

    ./manage.py migrate
    ./manage.py loaddata path/to/fedback/fixtures/*.json


How it works
-------------
A FeedbackForm contains one or more FormElement models of different ElementType.
The data is collected for each submission into FeedbackData.

As a form can be placed in different parts of a web resource, Placement records can be created to
group together form data submitted for different parts of the application. Placements do not have
to be created upfront, and can be generated on the fly by providing a unique placement key with the form.

A REST Api is exposed to allow manipulating the models externally, which is useful when this is deployed
into a backend service.

In addition, a view to accept form submissions is provided, as well as template tags to render a complete form
or part of it.

Forms can be built via the Api, Models or simply created via the Django admin or even fixtures.


Data collection
---------------
Data is collected into the ``FeedbackData`` model, grouped into ``FeedbackCollection`` entries.
As feedback forms can be used in different parts of an application, the model expects a ``Placement`` to tell
it which part of the application or website this form relates to. If a placement is not provided explicitly,
a default one will be used. Placement ids can also be provided in runtime by simply providing it as a string.
New ``Placement`` records will be created.


Settings
--------

The following settings are expected in your Django application::

    ===================== ================================================
    Setting               Description
    ===================== ================================================
    FEEDBACK_USER_MODEL   A path to the User model. Defaults to `auth.User`
    DEFAULT_PLACEMENT_KEY A key to use as default placement if one is not provided. Defaults to `DEFAULT`
    ===================== ================================================

Usage
-----

To include a complete feedback form::

    {% load feedback_form %}
    {% feedback_form request FORM_KEY_OR_ID %}

or to include a specific placement::

    {% feedback_form request FORM_KEY_OR_ID PLACEMENT_ID %}


Note that the feedback_form tag requires the request to pass through it in order toe generate the csrf_token.
