from rest_framework.permissions import IsAdminUser

from core.permissions import IsSeller, IsProductSeller


class IsAdminUserMixin:
    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class IsSellerMixin:
    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = [IsSeller]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class IsProductSellerMixin:
    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            permission_classes = [IsProductSeller]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
