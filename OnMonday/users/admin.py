from django.contrib import admin
from .models import User, UserEvents


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'email', 'gender', 'hobby', 'country')
    list_display_links = ('username', 'phone')


@admin.register(UserEvents)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_display_links = ('name', )

