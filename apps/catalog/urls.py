from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:category_slug>/', SubCategoriesList.as_view(), name='category-detail-view'),
    path('<slug:category_slug>/<slug:sub_category_slug>/', SubCategoryDetail.as_view(), name='subcategory-detail-view'),
    path('<slug:category_slug>/<slug:sub_category_slug>/<int:product_id>/', ProductDetail.as_view(),
         name='product-detail-view'),
    path('', CategoriesList.as_view(), name='categories'),
]
