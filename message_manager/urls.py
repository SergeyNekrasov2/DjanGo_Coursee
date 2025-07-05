from django.urls import path, include
from .views import MessageListView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView
from .apps import MessageManagerConfig

app_name = MessageManagerConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='messages_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('create/', MessageCreateView.as_view(), name='message_create'),
    path('<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

]