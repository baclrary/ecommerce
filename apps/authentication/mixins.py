from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from rest_framework import generics


class MessageMixin:
    """
    MessageMixin is a mixin that adds success and error message capabilities
    to Django form views. The success and error messages are displayed upon form validation.
    """
    success_message = None
    error_message = None

    def form_valid(self, form):
        """Handles success message upon valid form submission."""
        if self.success_message is not None:
            messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handles error messages upon invalid form submission."""
        if self.error_message is not None:
            messages.error(self.request, self.error_message)
        else:
            for error in form.errors.values():
                messages.error(self.request, error)
        return super().form_invalid(form)


class LoginOnValidMixin:
    """
    LoginOnValidMixin is a mixin that logs in the user upon valid form submission.
    """

    def form_valid(self, form):
        """Logs in the user upon valid form submission."""
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class RedirectIfNotAnonymousMixin(generics.GenericAPIView):
    """
    RedirectIfNotAnonymousMixin is a mixin that redirects authenticated users
    to a specific URL when they try to access the view. This is useful for pages
    like login or register, which should not be accessible for already authenticated users.
    """
    redirect_to = None

    def get(self, request, *args, **kwargs):
        """Redirects authenticated users to 'redirect_to' URL."""
        if not request.user.is_anonymous:
            return redirect(self.redirect_to)
        return super().get(request, *args, **kwargs)
