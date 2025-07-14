from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipient_manager.urls', namespace='home')),
    path('', include('message_manager.urls', namespace='message_manager')),
    path('', include('mailing.urls', namespace='mailing')),
    path('', include('users.urls', namespace='user')),

]