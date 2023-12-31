from django.db.models import Count
from django.views.generic import TemplateView

from catalog.models import Category, Product, Banner


class HomePage(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_products'] = Product.objects.filter(is_active=True).order_by('-id')[:4]
        context['top_products'] = Product.objects.annotate(review_count=Count('reviews')).filter(review_count__gt=0,
                                                                                                 is_active=True).order_by(
            '-review_count')[:8]
        context['banners'] = Banner.objects.all()

        return context
