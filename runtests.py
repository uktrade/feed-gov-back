#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    if len(sys.argv) == 4:
        settings.DATABASES['default']['NAME'] = sys.argv[1]
        settings.DATABASES['default']['USER'] = sys.argv[2]
        settings.DATABASES['default']['PASSWORD'] = sys.argv[3]
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
