from django import forms
from django.contrib.auth import get_user_model
from .models import Review, Product

class ReviewForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), widget=forms.HiddenInput())
    rating = forms.ChoiceField(choices=Review.RATING_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Review
        fields = ['title', 'review_text', 'rating', 'product', 'user']
