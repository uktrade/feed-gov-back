=============
Feed Gov Back
=============

A small API enabled framework for adding user feedback forms to existing applications within GOV.uk (or other apps).


Quick start
-----------

- Install the package::

    pip install feed-gov-back


- Add `feedback` to your ``INSTALLED_APPS`` in your ``settings``::

    INSTALLED_APPS = [
        ...
        'feedback',
    ]

- Include the feedback URLconf in your project urls.py like this::

    path('feedback/', include('feedback.services.urls'))

    or if not using the Api:

    path('feedback/', include('feedback.urls'))

- Run migrations and load fixtures::

    ./manage.py migrate
    ./manage.py loaddata path/to/fedback/fixtures/*.json


Using Make
----------
The ``Makefile`` provides some handy commands::

    make test  # run all tests
    make sdist  # run python setup.py sdist to create a local installable



How it works
-------------
A ``FeedbackForm`` contains one or more ``FormElement`` models of different ``ElementType``. These
models represent the form and it's elements.
The data is collected for each submission into ``FeedbackCollection`` which contain ``FeedbackData`` records for
each form element submitted.

As a form can be placed in different parts of a web resource, ``Placement`` records can be created to
group together form data submitted for different parts of the application. Placements do not have
to be created upfront, and can be generated on the fly by providing a unique placement key with the form.

A REST Api is exposed to allow manipulating the models externally, which is useful when this is deployed
into a backend service.

In addition, a view to accept form submissions is provided, as well as template tags to render a complete form
or part of it.

Forms can be built via the Api, Models or simply created via the Django admin or even fixtures.


Element Types
-------------
There are 3 element types defined: scale, large text area and text input. Scale elements can receive
``options`` to override defaults. The options and defaults are::

    {
        "min": 1,
        "max": 5,
        "min_label": "Poor",
        "max_label": "Excellent",
        "type": int
    }

    It is also possible to explicitly define the scale labels by providing a list of labels instead of the min/max
    combination

    ``labels: ["great", "indifferent", "poor"]``

    In this case the "type" property of the options should be changed to ``str``

Fields can be rendered by the ``form_element`` template tag provided or manually in your templates.


Data collection
---------------
Data is collected into the ``FeedbackData`` model, grouped into ``FeedbackCollection`` entries.
As feedback forms can be used in different parts of an application, the model expects a ``Placement`` to tell
it which part of the application or website this form relates to. If a placement is not provided explicitly,
a default one will be used. Placement ids can also be provided in runtime by simply providing it as a string.
New ``Placement`` records will be created.


Settings
--------

The following settings are expected in your Django application

======================= ================================================
Setting                 Description
======================= ================================================
AUTH_USER_MODEL         A path to the User model. Defaults to ``auth.User``
DEFAULT_PLACEMENT_KEY   A key to use as default placement if one is not provided. Defaults to ``DEFAULT``
ANONYMOUS_COLLECTION    A boolean to determine if to force anonymous collection or retain the user if available. Defaults to ``True``
MANAGED_FEEDBACK_MODELS Set to False to prevent the creation of database models. Defaults to ``True``
======================= ================================================

Usage
-----

To include a complete feedback form::

    {% load feedback_form %}
    {% feedback_form request 'FORM_REFERENCE' %}

or to include a specific placement::

    {% feedback_form request 'FORM_REFERENCE' 'PLACEMENT_ID' %}


Note that the feedback_form tag requires the request to pass through it in order toe generate the csrf_token.


*One important note* regarding FORM_REFERENCE shown in the tag example above: FORM_REFERENCE can be either a
Feedback form unique key, it's unique UUID, the form Model instance itself, or a dict representation of the form.
This allows for different usage pattern, depending on where this package is installed.
For example, if Feedback forms are to be used across a service which is made of an API and a UI layer as separate
applications, the API can install the package allowing for model creation but obviously not using the templatetags
as it has no rendering responsibility. The UI however can install the package, disabling model management and only
use the tags, by passing the dict returned from the API call. Note that in the case of passing a form model or dict
the single quotes should be omitted. The example application demonstrates this concept.


Styling
-------
The implemented template tags wrap the entire form in a div with id ``feedback-form``.
Subsequently, each element is div wrapped with a class ``feedback-form-element``.
The submit button is classed with ``feedback-form-button``.
Within each element the following divs wrap the name, label and description fields:
``feedback-form-element-name``, ``feedback-form-element-label`` and ``feedback-form-element-description``


Example App
-----------
The ``example`` directory contains a simple django project that utilises the feedback lib.
It provides a docker contained postgres db which can be built to isolate the example.
The make file allows for installation of the library based on a local sdist build.

To run it, create a virtual environment and activate it.
Then either provide your own database or ``docker-compose up`` to use the docker one.
Start with::

    ./manage.py migrate
    ./manage.py loaddata ./feed/fixtures/*.json
    ./manage.py runserver

- You can create your form via ``http://localhost:8000/admin`` (create a superuser to access the admin)
- interact with the form via ``http://localhost:8000``
- load the form using a key only: ``http://localhost:8000/key``
- load the form using a dict representation of it: ``http://localhost:8000/dict``
