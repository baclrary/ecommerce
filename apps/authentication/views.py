from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import LoginForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import *


class HomePageView(generic.TemplateView):
    """
    HomePageView is a view for the home page. If a user is authenticated,
    it shows the home page, otherwise, it redirects to the login page.
    """
    template_name = 'home.html'


class RegisterView(MessageMixin, generic.FormView):
    """
    RegisterView is a view for user registration. It displays a registration
    form and validates user input. Upon successful registration, the user is
    redirected to the login page with a success message.
    """
    template_name = 'pages/registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('authentication:login')
    success_message = "Account successfully created"

    def form_valid(self, form):
        user = form.save()
        # You can do anything you need with user object here (like login or send a confirmation email)
        return super().form_valid(form)


class LoginView(LoginOnValidMixin, MessageMixin, generic.FormView):
    """
    LoginView is a view for user login. It displays a login form and validates
    user input. Upon successful login, the user is redirected to the home page.
    In case of unsuccessful login attempt, an error message is displayed.
    """
    template_name = 'pages/registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    error_message = "Invalid email or password"


class LogoutView(LoginRequiredMixin, View):
    """
    LogoutView is a view for user logout. Upon accessing this view,
    the user is logged out and redirected to the home page. This view
    requires user authentication.
    """

    def get(self, request):
        """Handles GET request and logs out the user."""
        logout(request)
        return redirect('home')
