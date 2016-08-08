from django.contrib.sitemaps import Sitemap
from .models import Page


class PageSitemap(Sitemap):
    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        return obj.modified
