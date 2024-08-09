from django.urls import path
from .views import UserListAPI, UserDetail, google_auth, get_google_access_token, EventListView, \
    EventDetailView, EventCreateView, UserEventsView


urlpatterns = [
    path('list/', UserListAPI.as_view()),
    path('user_detail/<int:pk>/', UserDetail.as_view()),
    path('google_auth/', google_auth),
    path('get-google-access-token/', get_google_access_token),
    path('events/', EventListView.as_view()),
    path('events/<int:pk>/', EventDetailView.as_view()),
    path('events/create/', EventCreateView.as_view()),
    path('events/<int:pk>/register/', EventDetailView.as_view(http_method_names=['post'])),
    path('users/<int:pk>/events/', UserEventsView.as_view(), name='user_events'),
    path('users/<int:pk>/events/<int:event_id>/unregister/', UserDetail.as_view(http_method_names=['delete'])),
]

