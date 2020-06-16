from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProjectSerializer
from platform_app.models import Project
from rest_framework.views import APIView


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)

    user = User.objects.get(username=user)
    
    return Response({'token': token.key, 'user': user.id, 'username': user.username}, status=HTTP_200_OK)


class ProjectsApiView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.filter(user=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        projects = self.get_object(pk)
        Projects = ProjectSerializer(projects, context={"request": request}, many=True)
        return Response(Projects.data)
