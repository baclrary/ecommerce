# Models
from catalog.models import (
    Category,
    CategoryAttribute,
    Product,
    ProductAttribute,
    ProductFAQ,
    SubCategory,
)
from django.core.paginator import Paginator
from django.db.models import Case, Count, IntegerField, When
from django.http import JsonResponse

# Django
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import generic

# Forms
from review.forms import ReviewForm
from review.models import Reply, Review

# Models Views
from review.views import ReviewCreateView


class CategoriesList(generic.ListView):
    """
    This view handles displaying a list of all Categories.
    """
    template_name = 'catalog/categories_list.html'
    model = Category
    context_object_name = 'categories'


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
    # paginate_faq_by = 5
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
                - A list of the first batch of FAQs for the Product.

        """
        context = super().get_context_data(**kwargs)
        faqs = Paginator(self.get_faqs_for_product(), 5)  # Show 5 FAQs per page
        reviews = Paginator(self.get_reviews_for_product(), 5)  # Show 5 reviews per page

        context['attributes'] = self.get_attributes_for_product()
        context['review_form'] = self.get_review_form()
        context['faqs'] = faqs.get_page(1)  # Get first page
        context['faqs_count'] = faqs.count
        context['reviews'] = reviews.get_page(1)  # Get first page
        context['reviews_count'] = reviews.count
        # context['user_reactions'] = {review.id: review.get_user_reaction(self.request.user) for review in
        #                              context['reviews']}

        # permissions
        context['can_create_review'] = self.request.user.has_perm('review.add_review')

        # Check if the user has the 'add_review' permission
        # has_perm = self.request.user.has_perm('review.add_review')
        # print("User:", self.request.user)
        # print("Has add_review permission:", has_perm)
        # context['can_create_review'] = has_perm

        return context

    def get_faqs_for_product(self):
        """
        Returns a queryset of FAQs for the Product.
        """
        return ProductFAQ.objects.filter(product=self.get_object())

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

    def gather_reactions(self, replies):
        reactions = {}
        for reply in replies:
            reactions[reply.id] = reply.get_user_reaction(self.request.user)
            if reply.replies_to_reply.exists():
                reactions.update(self.gather_reactions(reply.replies_to_reply.all()))
        return reactions

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to create a new Review.
        """
        return ReviewCreateView.as_view()(request)

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # This is an AJAX request
            start = int(request.GET.get('start', 0))

            if request.GET.get('type') == 'faq':
                faqs = self.get_faqs_for_product()[start:start + 5]
                html = render_to_string('catalog/faq_items.html', {'faqs': faqs})
                has_more = self.get_faqs_for_product()[start + 5:start + 10].exists()
                return JsonResponse({'html': html, 'has_more': has_more})

            elif request.GET.get('type') == 'review':
                reviews = self.get_reviews_for_product()[start:start + 5]
                user_reactions = {}
                if request.user.is_authenticated:
                    user_reactions['reviews']: {review.id: review.get_user_reaction(request.user) for review in reviews}
                    user_reactions['replies']: self.gather_reactions(Reply.objects.filter(review__in=reviews))
                html = render_to_string('catalog/reviews_items.html',
                                        {'reviews': reviews, 'user_reactions': user_reactions, 'request': request})
                has_more = self.get_reviews_for_product()[start + 5:start + 10].exists()
                return JsonResponse({'html': html, 'has_more': has_more, 'user_reactions': user_reactions})

        context = self.get_context_data()
        return self.render_to_response(context)
