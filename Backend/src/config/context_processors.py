from catalog.models import Category


def site_settings(request):
    return {'menu_categories': Category.objects.all()}
