from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from catalog.models import Product

from .forms import ReviewForm


class ReviewCreateView(generic.View):
    form_class = ReviewForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.title = form.cleaned_data['title']
            new_review.product = get_object_or_404(Product, id=request.POST.get('product'))
            new_review.save()
            form.save()
            product_id = form.cleaned_data['product'].id
            category_slug = form.cleaned_data['product'].category.category.slug
            sub_category_slug = form.cleaned_data['product'].category.slug
            return HttpResponseRedirect(reverse('product-detail-view',
                                                kwargs={'product_id': product_id, 'category_slug': category_slug,
                                                        'sub_category_slug': sub_category_slug}))
        else:
            # you can redirect back to the product detail page or send a message that the form is invalid.
            print(form.errors)

            product_id = request.POST.get('product_id', None)
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                return HttpResponseRedirect(reverse('product-detail-view', kwargs={'product_id': product.id,
                                                                                   'category_slug': product.category.category.slug,
                                                                                   'sub_category_slug': product.category.slug}))
            else:
                return HttpResponse("Invalid form data", status=400)
