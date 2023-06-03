from rest_framework.decorators import api_view
from rest_framework.response import Response
from .search import Search
from .serializers import RegistrationSerializer
from rest_framework import generics
from django.views.generic import TemplateView


from catalog.models import Category


class HomePage(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_categories'] = Category.objects.all()
        return context


class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer


@api_view(["GET"])
def text_search(request):
    search = Search()
    return Response(search.text_search(request))


@api_view(["GET"])
def voice_search(request):
    search = Search()
    return Response(search.voice_search())
