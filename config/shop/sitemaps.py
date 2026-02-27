from django.contrib.sitemaps import Sitemap
from .models import Product, RentItem
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ['home', 'rent']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()


class RentItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return RentItem.objects.all()