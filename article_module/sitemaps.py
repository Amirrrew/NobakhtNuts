from django.contrib.sitemaps import Sitemap

from article_module.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Article.objects.filter(
            is_active=True
        )

    def location(self, obj):
        return obj.get_absolute_url()