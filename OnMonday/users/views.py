from django.shortcuts import render
from django.http import Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import status
from rest_framework.decorators import api_view
from social_django.views import login
import google.auth.transport.requests
import google.oauth2.id_token
from datetime import timedelta

from .models import User, UserEvents
from .serializers import UserSerializer, GoogleLoginSerializer, UserEventSerializer


print('Hello User!')


class UserListAPI(views.APIView):
    def get(self, request, pk=None): # Add 'pk=None' to the get method
        if pk is not None:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(views.APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_events(self, request, pk):
        """
            Получение списка участников мероприятия
        """
        user = self.get_object(pk)
        if user is None:
            return Response({'error': 'Пользователь не найден'},
                            status=status.HTTP_404_NOT_FOUND)

        events = user.events.all()
        serializer = UserEventSerializer(events, many=True)
        return Response(serializer.data)

    def delete_event(self, request, pk, event_id):
        """
            Отмена регистрации на мероприятие
        """
        user = User.objects.get(pk=pk)
        if user is None:
            return Response({'error': 'Пользователь не найден'},
                            status=status.HTTP_404_NOT_FOUND)

        event = UserEvents.objetcs.get(pk=event_id)
        if event is None:
            return Response({'error': 'Событие не найдено'},
                            status=status.HTTP_404_NOT_FOUND)

        event.users.remove(user)
        return Response({'message': 'Вы успешно отменили регистрацию на мероприятие'},
                        status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserEventsView(views.APIView):
    def get_events(self, request, pk):
        """
        Получение списка событий пользователя.
        """
        user = User.objects.get(pk=pk)
        if user is None:
            return Response({'error': 'Пользователь не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        events = user.user_events.all()  # Получаем события, к которым привязан пользователь
        serializer = UserEventSerializer(events, many=True)
        return Response(serializer.data)



@api_view(['POST'])
def google_auth(request):
    serializer = GoogleLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    access_token = serializer.validated_data['access_token']

    try:
        # Верифицируем токен доступа Google
        idinfo = google.oauth2.id_token.verify(access_token, google.auth.transport.requests.Request())

        # Получаем данные пользователя из токена
        user_data = {
            'user_id': idinfo['sub'],
            'email': idinfo['email'],
            'name': idinfo['name']
        }
    except ValueError:
        return Response({'error': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем или создаем пользователя на основе данных пользователя
    user = User.objects.get_or_create(username=user_data['user_id'])

    # Входим пользователя в систему
    login(request, user)

    return Response(serializer.data)


@api_view(['POST'])
def get_google_access_token(request):
    code = request.data.get('code')
    access_token = get_google_access_token(code)
    return Response({'access_token': access_token})


class EventListView(views.APIView):
    """
    Представление для получения списка мероприятий
    """
    def get(self, request):
        events = UserEvents.objects.all()
        serializer = UserEventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetailView(views.APIView):
    def get_object(self, pk):
        try:
            return UserEvents.objects.get(pk=pk)
        except UserEvents.DoesNotExist:
            return None

    def get(self, request, pk):
        event = self.get_object(pk)
        if event is None:
            return Response({'error': 'Событие не найдено'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserEventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        if event is None:
            return Response({'error': 'Событие не найдено'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserEventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        if event is None:
            return Response({'error': 'Событие не найдено'}, status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk):
        """
            Регистрация на мероприятие
        """
        event = UserEvents.objects.get(pk=pk)
        if event is None:
            return Response({'error': 'Событие не найдено'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user.is_authenticated:
            event.users.add(user)
            return Response({'message': 'Вы успешно зарегистрировались на мероприятие'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Необходимо авторизоваться'},
                            status=status.HTTP_401_UNAUTHORIZED)


class EventCreateView(views.APIView):
    """
        Представление для создания нового мероприятия
    """
    def post(self, request):
        serializer = UserEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



