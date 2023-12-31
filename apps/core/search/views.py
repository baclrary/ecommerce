from rest_framework.views import APIView
from rest_framework.response import Response
from .services import Search


class TextSearchView(APIView):
    def get(self, request):
        search = Search()
        return Response(search.text_search(request))


class VoiceSearchView(APIView):
    def get(self, request):
        search = Search()
        return Response(search.voice_search())
