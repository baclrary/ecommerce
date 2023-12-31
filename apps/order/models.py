import random
import string
from decimal import Decimal

from catalog.models import Product
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In progress'),
        ('delivering', 'Delivering'),
        ('canceled', 'Canceled'),
        ('closed', 'Closed')
    ]

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = PhoneNumberField(("phone"))
    address = models.TextField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=300)
    closed_at = models.DateTimeField(null=True, blank=True)
    total_sum = models.DecimalField(default=0, max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    order_number = models.CharField(max_length=10, unique=True, editable=False)

    def __str__(self):
        return "Order#" + str(self.id)

    @staticmethod
    def get_total_order_count_by_email(email: str):
        return Order.objects.filter(email=email).count()

    @staticmethod
    def get_closed_orders_item_total_by_email(email: str):
        orders = Order.objects.filter(email=email, status='closed')
        total_quantity = orders.annotate(total=Sum('orderitem__quantity')).aggregate(Sum('total'))['total__sum']
        return total_quantity or 0

    def _generate_order_number(self):
        """
        Generate 10 characters long order number. It is comprises two random letters as prefix and 8 digits.
        """
        prefix_letters = ''.join(random.choices(string.ascii_uppercase, k=2))  # Generate 2 random uppercase letters
        number = ''.join(random.choices(string.digits, k=8))  # Generate 8 random digits
        return prefix_letters + number

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate a new order number if one hasn't been set.
            self.order_number = self._generate_order_number()
            # If the generated order number is already in use, generate a new one
            while Order.objects.filter(order_number=self.order_number).exists():
                self.order_number = self._generate_order_number()
        super(Order, self).save(*args, **kwargs)

        if self.pk:  # Only calculate the total price if the order has been saved
            self.total_sum = sum(item.price for item in self.orderitem_set.all())
            super(Order, self).save(*args, **kwargs)  # Save the order again after calculating the total price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.order} - {self.product.title}"

    @property
    def price(self):
        return self.product.price * self.quantity
