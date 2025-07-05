from django.urls import path, include
from recipient_manager.apps import RecipientManagerConfig
from recipient_manager.views import (MailingRecipientListView, HomeView, MailingRecipientDetailView,
                                     MailingRecipientCreateView, MailingRecipientDeleteView, MailingRecipientUpdateView)


app_name = RecipientManagerConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recipients/', MailingRecipientListView.as_view(), name='recipient_list'),
    path('recipients/create/', MailingRecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/', MailingRecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='recipient_delete'),
    path('recipients/<int:pk>/update/', MailingRecipientUpdateView.as_view(), name='recipient_update'),
]