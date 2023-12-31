from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# View sets
import catalog.viewsets as catalog_view_sets
import review.viewsets as review_view_sets

# Views
import cart.views as cart_views
import core.views as core_views
import distribution.views as distribution_views
import order.views as order_views

# Schema setup
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Router setup
main_router = routers.DefaultRouter()

# Order related routes
# main_router.register(r'order', order_views.OrderViewSet, basename='order')
# main_router.register(r'order_item', order_views.OrderItemViewSet, basename='order_item')
main_router.register(r'top_sales', order_views.TopSalesAPIView, basename='top_sales')

# Catalog related routes
main_router.register(r'category', catalog_view_sets.CategoryViewSet, basename='category')
main_router.register(r'category_attribute', catalog_view_sets.CategoryAttributeViewSet, basename='category_attribute')
main_router.register(r'product', catalog_view_sets.ProductViewSet, basename='product')
main_router.register(r'product_attribute', catalog_view_sets.ProductAttributeViewSet, basename='product_attribute')

# Review related routes
main_router.register(r'review', review_view_sets.ReviewViewSet, basename='review')

# Cart related routes
main_router.register(r'cart', cart_views.CartViewSet, basename='cart')
main_router.register(r'cart_item', cart_views.CartItemViewSet, basename='cart_item')
main_router.register(r'wishlist', cart_views.WishlistViewSet, basename='wishlist')

# Distribution related routes
main_router.register(r'distribution', distribution_views.EmailDistributionViewSet, basename='distribution')
main_router.register(r'distribution_categories', distribution_views.DistributionCategoryViewSet, basename='distribution_categories')

urlpatterns = [
    path('', core_views.HomePage.as_view(), name='home'),
    path('', include("users.urls")),
    path('api/', include("rest_framework.urls")),
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('cart/', include("cart.urls"), name="cart"),
    path('categories/', include("catalog.urls"), name="catalog"),
    path('review/', include("review.urls"), name="review"),
    # path('api/v1/', include(main_router.urls)),
    # path('api/v1/authentication/', include("users.urls")),
    # path('checkout/', catalog_views.CheckoutSessionView.as_view(), name='checkout'),
    # path('stripe-session-completed/', catalog_views.stripe_session_completed_webhook, name='stripe-session-completed'),
    # path('success/', catalog_views.SuccessfulPayment.as_view(), name='success'),
    # path('api/v1/search/text/', core_views.text_search, name='text_search'),
    # path('api/v1/search/voice/', core_views.voice_search, name='voice_search'),
    # path("__reload__/", include("django_browser_reload.urls")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
