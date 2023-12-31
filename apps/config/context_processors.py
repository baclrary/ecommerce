from django.contrib.auth.models import Permission

from catalog.models import Category


def site_settings(request):
    return {'menu_categories': Category.objects.all()}


def add_permissions_to_context(request):
    perms = {'{}.{}'.format(perm.content_type.app_label, perm.codename): request.user.has_perm(
        '{}.{}'.format(perm.content_type.app_label, perm.codename)) for perm in Permission.objects.all()}
    return {'perms': perms}
