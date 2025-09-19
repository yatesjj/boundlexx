from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.azure_storage import AzureStorage


def select_storage(name):
    # Django 5.2 LTS: Use new STORAGES setting instead of deprecated setting
    storage_backend = settings.STORAGES.get("default", {}).get("BACKEND", "")
    if "AzureStorage" in storage_backend:
        return AzureStorage(azure_container=f"{settings.AZURE_CONTAINER_PREFIX}{name}")
    return FileSystemStorage()
