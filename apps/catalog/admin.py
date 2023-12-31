from django.contrib import admin

from .models import Category, CategoryAttribute, SubCategory, Product, ProductAttribute, Banner, ProductFAQ


class CategoryAttributeInline(admin.TabularInline):
    """
    Provides inline editing of CategoryAttributes in the SubCategory admin view.
    """
    model = CategoryAttribute.category.through
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    """
    Provides inline editing of ProductAttributes in the Product admin view.
    """
    model = ProductAttribute
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Category model.
    Includes fields in the list view and enables slug auto-population from the title.
    """
    list_display = ['id', 'title']
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ['title']


class SubCategoryAdmin(admin.ModelAdmin):
    """
    Custom admin view for the SubCategory model.
    Includes fields in the list view, enables slug auto-population from the title,
    and provides inline editing of CategoryAttributes.
    """
    list_display = ['id', 'title', 'category']
    prepopulated_fields = {'slug': ('title',), }
    inlines = [CategoryAttributeInline]
    list_filter = ['category']
    search_fields = ['title']


class ProductAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Product model.
    Provides inline editing of ProductAttributes.
    """
    list_display = ['id', 'title', 'category', 'count', 'base_price', 'is_active']
    inlines = [ProductAttributeInline]
    list_filter = ['category', 'is_active']
    search_fields = ['title']


class CategoryAttributeAdmin(admin.ModelAdmin):
    """
    Custom admin view for the CategoryAttribute model.
    """
    list_display = ['id', 'name']
    search_fields = ['name']


class ProductAttributeAdmin(admin.ModelAdmin):
    """
    Custom admin view for the ProductAttribute model.
    """
    list_display = ['id', 'product', 'attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['value', 'attribute__name', 'product__title']


class BannerAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Banner model.
    """
    list_display = ['id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CategoryAttribute, CategoryAttributeAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(ProductFAQ)