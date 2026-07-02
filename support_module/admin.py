from django.contrib import admin

from support_module.models import Ticket, TicketReason, TicketStatus, SupportWays, Questions, QuestionCategory


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title' ,'reason' ,'status' ,'created_at']
    list_editable = ['status' ,]
    list_filter = ['created_at' ,'status' ,]

class QuestionAdmin(admin.TabularInline):
    model = Questions
    extra = 1

class QuestionsCatAdmin(admin.ModelAdmin):
    inlines = [QuestionAdmin]

admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketReason)
admin.site.register(TicketStatus)
admin.site.register(SupportWays)
admin.site.register(QuestionCategory ,QuestionsCatAdmin)
