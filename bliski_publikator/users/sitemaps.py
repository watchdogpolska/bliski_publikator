from django.contrib.sitemaps import Sitemap
from .models import User


class UserSitemap(Sitemap):
    def items(self):
        return User.objects.all()
