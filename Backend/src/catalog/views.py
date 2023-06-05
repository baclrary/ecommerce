# Models
from review.models import Review
from catalog.models import Category, Product, CategoryAttribute, ProductAttribute, SubCategory

# Models Views
from review.views import ReviewCreateView

# Django
from django.shortcuts import get_object_or_404
from django.views import generic

# Forms
from review.forms import ReviewForm


def get_menu_categories():
    """
    Returns a queryset containing all Category objects.
    This is used for populating the menu in various views.
    """
    return Category.objects.all()


class CategoriesList(generic.ListView):
    """
    This view handles displaying a list of all Categories.
    """
    template_name = 'catalog/categories_list.html'
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_categories'] = get_menu_categories()
        return context


class SubCategoriesList(generic.ListView):
    """
    This view handles displaying a list of SubCategories within a given Category.
    """
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
        context['menu_categories'] = get_menu_categories()
        return context


class SubCategoryDetail(generic.DetailView):
    """
    This view handles the display of a detailed SubCategory page.
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
        context['attributes'] = self.get_attributes_for_subcategory()
        context['category_slug'] = self.kwargs['category_slug']
        context['menu_categories'] = get_menu_categories()
        context['products'] = self.get_filtered_products_for_subcategory()

        return context

    def get_attributes_for_subcategory(self):
        """
        Returns a dictionary of category_attributes for the SubCategory and their unique values.
        """
        category_attributes = self.object.attributes.all().prefetch_related('attributes_values')
        attribute_dict = {}
        for attribute in category_attributes:
            attribute_dict[attribute] = list(
                set([product_attr.value for product_attr in attribute.attributes_values.all()]))

        return attribute_dict

    def get_filtered_products_for_subcategory(self):
        """
        Returns a queryset of Products for the SubCategory based on the selected filters in the GET request.
        """
        sub_category = self.object
        products = Product.objects.filter(category=sub_category, is_active=True)

        for category_attribute in CategoryAttribute.objects.filter(category=sub_category):
            attribute_values = self.request.GET.getlist(f"{category_attribute.name}-{category_attribute.id}")

            if attribute_values:
                products = products.filter(attributes__attribute=category_attribute,
                                           attributes__value__in=attribute_values)

        return products


class ProductDetail(generic.DetailView):
    """
    This view handles the display of a detailed Product page.
    """
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    model = Product

    def get_object(self):
        """
        Overrides the get_object method to retrieve the desired Product object by id.
        """
        return get_object_or_404(Product, id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        """
        Overrides the get_context_data method to add additional context data:
        - A list of Reviews for the Product.
        - A dictionary of the Product's attributes.
        - An empty Review form.
        """
        context = super().get_context_data(**kwargs)
        context['menu_categories'] = get_menu_categories()
        context['attributes'] = self.get_attributes_for_product()
        context['reviews'] = self.get_reviews_for_product()
        context['review_form'] = self.get_review_form()

        return context

    def get_reviews_for_product(self):
        """
        Returns a queryset of Reviews for the Product.
        """
        return Review.objects.filter(product=self.get_object())

    def get_attributes_for_product(self):
        """
        Returns a dictionary of the Product's attributes.
        """
        product = self.get_object()
        attribute_dict = {}
        for attr in product.attributes.all():
            attribute_dict.setdefault(attr.attribute.name, []).append(attr.value)

        return attribute_dict

    def get_review_form(self):
        """
        Returns an empty Review form.
        """
        product = self.get_object()
        return ReviewForm(initial={'product': product, 'user': self.request.user})

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to create a new Review.
        """
        return ReviewCreateView.as_view()(request)
