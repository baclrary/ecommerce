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
