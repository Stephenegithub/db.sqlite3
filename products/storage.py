from typing import Optional, Any

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured

PROTECTED_MEDIA: Optional[Any] = getattr(settings, 'PROTECTED_MEDIA', None)
if PROTECTED_MEDIA is None:
    raise ImproperlyConfigured("PROTECTED_MEDIA is not set in settings.py")


# django-storages
class ProtectedStorage(FileSystemStorage):
    location = PROTECTED_MEDIA  # MEDIA_ROOT
