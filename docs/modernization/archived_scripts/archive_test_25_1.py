#!/usr/bin/env python
import sys
import os

# Force use of the local installation
sys.path.insert(0, "/home/django/.local/lib/python3.12/site-packages")

import django_filters

print(f"Version: {django_filters.__version__}")

from django_filters.rest_framework import DjangoFilterBackend

backend = DjangoFilterBackend()
has_method = hasattr(backend, "get_schema_operation_parameters")
print(f"Has get_schema_operation_parameters method: {has_method}")

if not has_method:
    print("Available methods:", [m for m in dir(backend) if not m.startswith("_")])
else:
    print("Method exists - testing actual schema generation...")

    # Now test actual usage
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    import django

    django.setup()

    try:
        from rest_framework.request import Request
        from django.test import RequestFactory
        from boundlexx.api.v1.views.item import ItemViewSet

        # Create a test request
        factory = RequestFactory()
        request = factory.get("/api/v1/items/")

        # Create view instance
        view = ItemViewSet()
        view.request = Request(request)
        view.format_kwarg = None

        # Try to get schema operation parameters
        result = backend.get_schema_operation_parameters(view, request)
        print(f"Schema generation successful: {len(result)} parameters")

    except Exception as e:
        print(f"Schema generation FAILED: {e}")
        print(f"Error type: {type(e).__name__}")
