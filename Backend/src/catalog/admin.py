from django.contrib import admin

from .models import Category, CategoryAttribute, SubCategory, Product, ProductAttribute, Banner


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    prepopulated_fields = {'slug': ('title',), }


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register([CategoryAttribute, Product, ProductAttribute, Banner])
