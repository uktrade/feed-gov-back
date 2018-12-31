# feed-gov-back
A small framework for adding API enabled user feedback forms


## Installation and Setup

To install the package:

`
pip install feed-gov-back
`

Add `feedback` to your `INSTALLED_APPS` in your `settings`.
In your main `urls` file, add:

`
path('feedback/', include('feedback.services.urls'))
`

to include all the feedback form API urls. You can configure the base path as suits your application.
