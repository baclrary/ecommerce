from django.urls import reverse_lazy
from django.views.generic import TemplateView
from order.models import Order, OrderItem
from review.models import Review
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = 'pages/users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_orders_number'] = Order.get_closed_orders_item_total_by_email(self.request.user.email)
        context['user_reviews_number'] = Review.get_user_total_reviews_count(self.request.user)
        return context


class UserInfo(LoginRequiredMixin, TemplateView):
    template_name = 'pages/users/user_info.html'


class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'pages/users/orders.html'
    context_object_name = 'user_orders'

    def get_queryset(self):
        return Order.objects.filter(email=self.request.user.email)

#
# class OrderDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Order
#     template_name = "order_detail.html"
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#
# class OrderCreateView(LoginRequiredMixin, generic.CreateView):
#     model = Order
#     template_name = "order_form.html"
#     fields = ['first_name', 'last_name', 'email', 'phone', 'address']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#
# class OrderItemCreateView(LoginRequiredMixin, generic.CreateView):
#     model = OrderItem
#     template_name = "orderitem_form.html"
#     fields = ['order', 'product', 'quantity']
#
#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['order'].queryset = Order.objects.filter(user=self.request.user)
#         return form
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
#
# class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
#     model = Order
#     template_name = "order_form.html"
#     fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'status', 'closed_at']
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
#
#
# class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
#     model = Order
#     template_name = "order_confirm_delete.html"
#     success_url = reverse_lazy('orders')
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
