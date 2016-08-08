from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home', 'contact', 'api-root']

    def location(self, item):
        return reverse(item)
