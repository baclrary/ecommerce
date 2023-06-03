from django.contrib import admin
from .models import User, SellerProfile, BuyerProfile

admin.site.register([User, SellerProfile, BuyerProfile])