from django.contrib import admin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth')
    search_fields = ('user__email', 'first_name', 'middle_name', 'last_name')
    ordering = ('user',)
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'photo')}),
        ('Distributions', {'fields': ('distributions',)}),
    )
