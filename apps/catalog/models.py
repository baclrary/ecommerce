from decimal import Decimal
from statistics import mean

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from .permissions import (
    banner_permissions,
    category_permissions,
    categoryattribute_permissions,
    product_permissions,
    productattribute_permissions,
    subcategory_permissions,
)


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    icon = models.ImageField(default="assets/category_icons/default_category_icon.png", upload_to="category_icons/",
                             blank=True, null=True, max_length=255, verbose_name="Header Icon")
    image = models.ImageField(blank=True, null=True, verbose_name="Category Image")
    description = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Categories'
        permissions = category_permissions

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        if not self.image and self.icon:
            self.image = self.icon

        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=120, allow_unicode=True)
    category = models.ForeignKey(Category, related_name='subcategory', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(default="assets/sub_category_images/default_sub_category.png",
                              upload_to="sub_category_images/", blank=True, null=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Sub Categories'
        permissions = subcategory_permissions

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(SubCategory, self).save(*args, **kwargs)


class CategoryAttribute(models.Model):
    category = models.ManyToManyField(SubCategory, related_name='attributes')
    name = models.CharField(max_length=200)

    class Meta:
        permissions = categoryattribute_permissions

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    count = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to='product_images', default='assets/product_images/default_product.png',
                              blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=get_user_model(), related_name='seller', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)
        permissions = product_permissions

    def __str__(self):
        attributes = ' / '.join(product_attribute.value for product_attribute in self.attributes.all())
        return f"{self.title} {attributes}"

    @property
    def price(self):
        try:
            product_on_promotions = self.product_on_promotion.get(promotion_id__is_active=True)
            return product_on_promotions.promo_price
        except ObjectDoesNotExist:
            return self.base_price

    def get_product_rating(self):
        ratings = [review.rating for review in self.reviews.all()]
        return mean(ratings) if ratings else None


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE, related_name="attributes_values")
    value = models.CharField(max_length=200)

    class Meta:
        permissions = productattribute_permissions

    def __str__(self):
        return f"{self.product}. {self.attribute}: {self.value}"


class ProductFAQ(models.Model):
    product = models.ForeignKey(Product, related_name='faq', on_delete=models.CASCADE)
    question = models.CharField(max_length=250, blank=False, null=True)
    answer = models.CharField(max_length=1000, blank=False, null=True)

    def __str__(self):
        return f"{self.question} - {self.answer}"


class Banner(models.Model):
    image = models.ImageField(upload_to='slider_images', default='assets/banners/0.webp',
                              blank=True, null=True)

    class Meta:
        permissions = banner_permissions

    def __str__(self):
        return f"Banner - {self.id}"
