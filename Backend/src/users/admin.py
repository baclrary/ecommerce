from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, BuyerProfile, SellerProfile


class ProfileInline(admin.StackedInline):
    model = CustomUser.profile.related.related_model  # This will get the related Profile model (BuyerProfile or SellerProfile)
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('email', 'type', 'is_staff', 'is_active',)
    list_filter = ('email', 'type', 'is_staff', 'is_active',)
    search_fields = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('type', 'phone')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'type', 'phone'),
        }),
    )
    ordering = ('email',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'middle_name', 'last_name']
    search_fields = ['user__email', 'first_name', 'middle_name',
                     'last_name']  # search by email, name, middle name or last name


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BuyerProfile, ProfileAdmin)
admin.site.register(SellerProfile, ProfileAdmin)
