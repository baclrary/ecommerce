from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Category, SubCategory, Product
from .views import CategoriesList, SubCategoriesList, SubCategoryDetail, ProductDetail
from decimal import Decimal


class CatalogTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.category = Category.objects.create(title='Test Category', description='Test Description')
        cls.subcategory = SubCategory.objects.create(title='Test Subcategory', category=cls.category)
        user = get_user_model().objects.create(email='testuser@test.com')
        cls.product = Product.objects.create(
            title='Test Product',
            category=cls.subcategory,
            base_price=Decimal('10.00'),
            created_by=user
        )

    def test_categories_list_view(self):
        url = reverse('categories')
        request = self.factory.get(url)
        response = CategoriesList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_subcategories_list_view(self):
        url = reverse('category-detail-view', kwargs={'category_slug': self.category.slug})
        request = self.factory.get(url)
        response = SubCategoriesList.as_view()(request, category_slug=self.category.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subcategory')

    def test_subcategory_detail_view(self):
        url = reverse('subcategory-detail-view',
                      kwargs={'category_slug': self.category.slug, 'sub_category_slug': self.subcategory.slug})
        request = self.factory.get(url)
        response = SubCategoryDetail.as_view()(request, category_slug=self.category.slug,
                                               sub_category_slug=self.subcategory.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subcategory')

    def test_product_detail_view(self):
        url = reverse('product-detail-view',
                      kwargs={'category_slug': self.category.slug, 'sub_category_slug': self.subcategory.slug,
                              'product_id': self.product.id})
        request = self.factory.get(url)
        request.user = get_user_model().objects.create(
            email='testuser@test.com')
        response = ProductDetail.as_view()(request, category_slug=self.category.slug,
                                           sub_category_slug=self.subcategory.slug, product_id=self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
