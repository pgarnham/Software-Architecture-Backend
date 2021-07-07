from chat.models import Message, User, Room
from chat.serializers import MessageSerializer, UserSerializer, RoomSerializer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import HttpResponse
import django_filters
from .APIConnection import APIPOST
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
class GoogleLogin(SocialLoginView):
    print("im in google login social view.")
    adapter_class = GoogleOAuth2Adapter


class RoomViewSet(viewsets.ModelViewSet):
    print("hello world im in rooms view")
    # permission_classes = (IsAuthenticated,)
    queryset = Room.objects.all()
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    serializer_class = RoomSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


    def delete(self, request, pk, format=None):
        room = self.get_object(pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args,**kwargs):

        room_object = self.get_object()
        room_object.name = request.data.get('name')
        room_object.is_private = request.data.get('is_private')
        room_object.save()
        serializer = self.get_serializer(room_object)
        self.perform_update(serializer)
        return Response(serializer.data)



class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    serializer_class = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


    def get_queryset(self):
        queryset = User.objects.all()
        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(email=email)
        return queryset

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args,**kwargs):

        user_object = self.get_object()
        user_object.username = request.data.get('username')
        user_object.is_admin = request.data.get('is_admin')
        user_data = JSONParser().parse(request)
        serializer = UserSerializer(user_object,data=user_data)
        if serializer.is_valid():
            serializer.save()  
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    serializer_class = MessageSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


    def get_queryset(self):
        queryset = Message.objects.all()
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author=author)
        room = self.request.query_params.get('room', None)
        if room is not None:
            queryset = queryset.filter(room=room)

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset


    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            print(request.POST.get('room', 123))
            APIPOST(request.POST['room'], request.POST['content'], request.POST['author'])
        response = super().dispatch(request, *args, **kwargs)
        return response

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
