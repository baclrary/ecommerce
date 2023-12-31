from rest_framework.viewsets import ModelViewSet

from catalog.models import Category, CategoryAttribute, Product, ProductAttribute
from catalog.serializers import CategorySerializer, CategoryAttributeSerializer, ProductSerializer, \
    ProductAttributeSerializer

from core.mixins import IsAdminUserMixin, IsSellerMixin, IsProductSellerMixin


class CategoryViewSet(ModelViewSet, IsAdminUserMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryAttributeViewSet(ModelViewSet, IsAdminUserMixin):
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer


class ProductViewSet(ModelViewSet, IsSellerMixin, IsProductSellerMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductAttributeViewSet(ModelViewSet, IsSellerMixin, IsProductSellerMixin):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
