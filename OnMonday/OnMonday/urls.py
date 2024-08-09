from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # path('google-login/', google_login, name='google_login'),
    path('', include('social_django.urls', namespace='social')),

    path('users/', include('users.urls')),
]

