#!/usr/bin/env python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django_filters.rest_framework import DjangoFilterBackend


def check_method_exists():
    backend = DjangoFilterBackend()

    # Check if the method exists
    has_method = hasattr(backend, "get_schema_operation_parameters")
    print(
        f"DjangoFilterBackend has 'get_schema_operation_parameters' method: {has_method}"
    )

    if has_method:
        print("Method signature:", backend.get_schema_operation_parameters.__doc__)
    else:
        print("Available methods:", [m for m in dir(backend) if not m.startswith("_")])

    # Check django-filter version
    import django_filters

    print(f"django-filter version: {django_filters.__version__}")


if __name__ == "__main__":
    check_method_exists()
