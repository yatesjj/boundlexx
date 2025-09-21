#!/usr/bin/env python
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from boundlexx.api.schemas import BoundlexxSchemaGenerator
from django.test import RequestFactory


def test_schema_generation():
    generator = BoundlexxSchemaGenerator()
    request = RequestFactory().get("/api/v1/schema/")
    request.version = "v1"

    try:
        schema = generator.get_schema(request=request)
        print("SUCCESS: Schema generation works with current django-filter version")
        print(f'Found {len(schema.get("paths", {}))} API paths')
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


if __name__ == "__main__":
    test_schema_generation()
