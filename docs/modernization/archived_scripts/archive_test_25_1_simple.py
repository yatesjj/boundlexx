#!/usr/bin/env python
import sys
import os

# Remove system packages to force local installation
sys.path = [p for p in sys.path if "site-packages" not in p or "local" in p]
sys.path.insert(0, "/home/django/.local/lib/python3.12/site-packages")

try:
    import django_filters

    print(f"Version: {django_filters.__version__}")

    from django_filters.rest_framework import DjangoFilterBackend

    backend = DjangoFilterBackend()
    has_method = hasattr(backend, "get_schema_operation_parameters")
    print(f"Has get_schema_operation_parameters method: {has_method}")

    if not has_method:
        print(
            "Method MISSING - Available methods:",
            [m for m in dir(backend) if not m.startswith("_")],
        )
    else:
        # Check method signature
        import inspect

        sig = inspect.signature(backend.get_schema_operation_parameters)
        print(f"Method signature: {sig}")
        print("Method exists but may have breaking signature changes")

except Exception as e:
    print(f"Import or basic test failed: {e}")
    print(f"Error type: {type(e).__name__}")
    print(f"Python path: {sys.path[:3]}")
