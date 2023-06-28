from django.conf import settings


def crispy_forms_settings(request):
    """
    Adds the CRISPY_TEMPLATE_PACK setting to the context.
    """
    return {'CRISPY_TEMPLATE_PACK': settings.CRISPY_TEMPLATE_PACK}