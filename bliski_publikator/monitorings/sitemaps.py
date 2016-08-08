from django.contrib.sitemaps import Sitemap
from .models import Monitoring, MonitoringInstitution


class MonitoringSitemap(Sitemap):
    def items(self):
        return Monitoring.objects.all()

    def lastmod(self, obj):
        return obj.modified


class MonitoringInstitutionSitemap(Sitemap):
    def items(self):
        return MonitoringInstitution.objects.all()
