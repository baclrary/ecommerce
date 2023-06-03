# DRF
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from catalog.serializers import CategorySerializer, ProductSerializer, CategoryAttributeSerializer, \
    ProductAttributeSerializer
from core.permissions import IsSeller, IsProductSeller

# Models
from cart.models import Cart
from review.models import Review
from order.models import Order, OrderItem
from catalog.models import Category, Product, CategoryAttribute, ProductAttribute, SubCategory

# Models Views
from cart.views import get_cart_from_session
from review.views import ReviewCreateView

# Django
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views import View
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# Forms
from review.forms import ReviewForm

# Stripe
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class CategoryAttributeViewSet(ModelViewSet):
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class SubCategoriesList(generic.ListView):
    template_name = "catalog/category_detail.html"
    context_object_name = "sub_categories"
    model = SubCategory

    def get_queryset(self):
        """
        Overrides the get_queryset method to retrieve only SubCategories
        belonging to the Category specified by the slug in the URL.
        """
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return SubCategory.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_categories'] = Category.objects.all()
        return context


class SubCategoryDetail(generic.DetailView):
    """
    This is a DetailView for SubCategory. It provides context for a template
    to show detailed information about a specific SubCategory including its related
    Products, Attributes, and the specific Filters for its Products.
    """
    template_name = "catalog/sub_category_detail.html"
    context_object_name = "sub_category"
    model = SubCategory

    def get_object(self):
        """
        Overrides the get_object method to use slugs in the URL to retrieve the desired SubCategory object.
        """
        return get_object_or_404(SubCategory, category__slug=self.kwargs['category_slug'],
                                 slug=self.kwargs['sub_category_slug'])

    def get_context_data(self, **kwargs):
        """
        Overrides the get_context_data method to add additional context data:
        - A dictionary of category_attributes for the SubCategory and their unique values.
        - A filtered queryset of Products for the SubCategory based on the selected filters in the GET request.
        """
        context = super().get_context_data(**kwargs)

        # Add all CategoryAttributes for this SubCategory to the context
        category_attributes = self.object.attributes.all()
        attribute_dict = {}
        for attribute in category_attributes:
            attribute_dict[attribute] = list(
                set([product_attr.value for product_attr in attribute.attributes_values.all()]))

        context['attributes'] = attribute_dict
        context['category_slug'] = self.kwargs['category_slug']
        context['menu_categories'] = Category.objects.all()

        # Start with all Products for this SubCategory
        sub_category = self.object
        products = Product.objects.filter(category=sub_category)

        # Now, we iterate over each attribute and its selected values
        for category_attribute in CategoryAttribute.objects.filter(category=sub_category):
            attribute_values = self.request.GET.getlist(f"{category_attribute.name}-{category_attribute.id}")

            if attribute_values:
                # This time, instead of combining the Q objects with OR,
                # we directly apply the filter to the products queryset for each attribute
                products = products.filter(attributes__attribute=category_attribute,
                                           attributes__value__in=attribute_values)

        # We no longer need to combine Q objects or use distinct,
        # as we're filtering the products queryset directly in the loop
        context['products'] = products

        return context


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = [IsSeller]
        elif self.action in ("update", "partial_update"):
            permission_classes = [IsProductSeller]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductAttributeViewSet(ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = [IsSeller]
        elif self.action in ("update", "partial_update"):
            permission_classes = [IsProductSeller]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class ProductDetail(generic.DetailView):
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    model = Product

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(product=self.get_object())

        # get product attributes
        product = self.get_object()
        attribute_dict = {}

        # Loop through all product attributes
        for attr in product.attributes.all():
            # Check if attribute name already exists in the dictionary
            if attr.attribute.name in attribute_dict:
                # If it exists, append the value
                attribute_dict[attr.attribute.name].append(attr.value)
            else:
                # If it doesn't exist, create a new list with the value
                attribute_dict[attr.attribute.name] = [attr.value]

        context['menu_categories'] = Category.objects.all()
        context['attributes'] = attribute_dict
        context['reviews'] = reviews
        context['review_form'] = ReviewForm(initial={'product': product, 'user': self.request.user})

        return context

    def post(self, request, *args, **kwargs):
        return ReviewCreateView.as_view()(request)


class SuccessfulPayment(generic.TemplateView):
    template_name = 'success.html'


class CheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        cart = get_cart_from_session(self.request)

        if not cart.cart_items.all():
            return HttpResponse({"Sorry, you don't have anything in your card"})

        total_sum = sum([cart_item.price for cart_item in cart.cart_items.all()])

        return render(request, "checkout.html", context={
            "cart": cart,
            "total_sum": total_sum,
            'checkout_public_key': settings.STRIPE_TEST_PUBLIC_KEY
        })

    def validate_request(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not all([first_name, last_name, email, phone]):
            raise ValueError('All fields are required.')

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Invalid email.')

        return first_name, last_name, email, phone

    def create_checkout_session(self, request, cart, total_sum, email, first_name, last_name, phone, address):
        line_items = []

        for cart_item in cart.cart_items.all():
            line_item = {
                'price_data': {
                    'currency': 'uah',
                    'unit_amount': int(cart_item.product.price * 100),
                    'product_data': {
                        'name': cart_item.product.title,
                        'images': [request.build_absolute_uri(
                            cart_item.product.image)] if cart_item.product.image and cart_item.product.image else [],
                    },
                },
                'quantity': cart_item.quantity,
            }
            line_items.append(line_item)

        return stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri(''),
            customer_email=email,
            metadata={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "address": address,
                "total_sum": total_sum,
                "cart_id": str(cart.id),
            }
        )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            first_name, last_name, email, phone = self.validate_request(request)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        address = request.POST.get('address')
        total_sum = request.POST.get('total_sum')

        cart = get_cart_from_session(self.request)
        checkout_session = self.create_checkout_session(request, cart, total_sum, email, first_name, last_name, phone,
                                                        address)

        return JsonResponse({'sessionId': checkout_session.id})


@csrf_exempt
def stripe_session_completed_webhook(request, *args, **kwargs):
    CHECKOUT_SESSION_COMPLETED = "checkout.session.completed"
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    except ValueError:
        return HttpResponse(status=400)

    if event["type"] == CHECKOUT_SESSION_COMPLETED:
        session = event['data']['object']
        metadata = session.get('metadata', {})

        if not metadata:
            return HttpResponse(status=400)

        cart = Cart.objects.get(id=metadata.get('cart_id'))

        # Create the order
        order = Order.objects.create(
            first_name=metadata.get('first_name'),
            last_name=metadata.get('last_name'),
            email=metadata.get('email'),
            phone=metadata.get('phone'),
            address=metadata.get('address'),
            total_sum=metadata.get('total_sum'),
            status='open'
        )

        # Create order's items
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )

        cart.cart_items.all().delete()
        return HttpResponse(status=200)
