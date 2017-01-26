from rest_framework.views import APIView
from rest_framework.response import Response

class LandingView(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response({"documentation": "Please see https://github.com/Axiologue/MindfulClickAPI for information on how to use this API"})
