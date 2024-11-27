from django.conf import settings

def enable_microsoft_oauth(request):
    return {
        'ENABLE_MICROSOFT_OAUTH': getattr(settings, 'ENABLE_MICROSOFT_OAUTH', False),
    }
