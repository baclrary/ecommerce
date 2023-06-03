from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from rest_framework import viewsets, status
from rest_framework.response import Response

from catalog.models import Product
from core.permissions import IsAuthenticated
from .serializers import ReviewSerializer
from .models import Review
from .forms import ReviewForm


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({'message': 'Not found', 'status': '404'}, status=status.HTTP_404_NOT_FOUND, )
        return super(ReviewViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({'message': 'Not found', 'status': '404'}, status=status.HTTP_404_NOT_FOUND, )
        return super(ReviewViewSet, self).destroy(request, *args, **kwargs)


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
