from django.contrib.sitemaps import Sitemap
from .models import Institution


class InstitutionSitemap(Sitemap):
    def items(self):
        return Institution.objects.all()

    def lastmod(self, obj):
        return obj.modified
