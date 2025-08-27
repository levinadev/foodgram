# tags/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class TagsStubView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response([])  # пустой список тегов
