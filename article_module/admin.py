from django.contrib import admin

from article_module.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title' ,'author' ,'created_at' ,'is_active']
    list_filter = ['created_at' ,'is_active']

admin.site.register(Article ,ArticleAdmin)
