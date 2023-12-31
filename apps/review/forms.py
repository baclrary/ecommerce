from django import forms
from django.contrib.auth import get_user_model
from .models import Review, Reply, Product
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), widget=forms.HiddenInput())
    rating = forms.ChoiceField(choices=Review.RATING_CHOICES, widget=forms.RadioSelect())

    def clean_media_files(self):
        files = self.files.getlist('media_files')

        if len(files) > 10:
            raise forms.ValidationError("You can only upload a maximum of 10 files.")

        for file in files:
            if file.size > 6 * 1024 * 1024:
                raise forms.ValidationError(
                    f"File '{file.name}' is larger than 6MB. Please upload a smaller file or compress it.")

        return files

    class Meta:
        model = Review
        fields = ['title', 'review_text', 'rating', 'product', 'user']


class ReplyAdminForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        review = cleaned_data.get("review")
        parent_reply = cleaned_data.get("parent_reply")

        if (not review and not parent_reply) or (review and parent_reply):
            raise ValidationError('Either review or parent_reply must be set, not both.')


class ReplyForm(forms.ModelForm):
    review = forms.ModelChoiceField(queryset=Review.objects.all(), widget=forms.HiddenInput(), required=False)
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), widget=forms.HiddenInput())
    parent_reply = forms.ModelChoiceField(queryset=Reply.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Reply
        fields = ['reply_text', 'review', 'user', 'parent_reply']
