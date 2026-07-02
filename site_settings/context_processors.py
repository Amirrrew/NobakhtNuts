from site_settings.models import SiteSettings


def site_settings(request):
    return {
        'site_settings': SiteSettings.objects.filter(is_default=True).first()
    }