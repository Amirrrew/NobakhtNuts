from django.contrib import admin
from .models import User, Address, Notification


class UserAdmin(admin.ModelAdmin):
    list_display = ['username' ,'phone' ,'is_active' ,]
    list_filter = ['created_at' ,]

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user' ,'details' ,]

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user' ,'title','is_seen' ,'is_read']
    list_filter = ['is_read' ,'created_at']


admin.site.register(User, UserAdmin)
admin.site.register(Address ,AddressAdmin)
admin.site.register(Notification, NotificationAdmin)

