from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return [
            "home",
            'about_us',
            'support_page'
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            "home": 1.0,
            "about_us": 0.4,
            "support_page": 0.4,
        }

        return priorities.get(item, 0.5)