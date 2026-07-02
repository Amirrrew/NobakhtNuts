from django.contrib import admin

from site_settings.models import SiteSettings, FooterLink, FooterLinkBox


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title' ,'is_default']


admin.site.register(SiteSettings , SettingAdmin)
admin.site.register(FooterLinkBox)
admin.site.register(FooterLink)