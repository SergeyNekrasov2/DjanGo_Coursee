from django.urls import path

from recipient_manager.apps import RecipientManagerConfig
from recipient_manager.views import (MailingRecipientListView, HomeView, MailingRecipientDetailView,
                                     MailingRecipientCreateView, MailingRecipientDeleteView, MailingRecipientUpdateView)

app_name = RecipientManagerConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', MailingRecipientListView.as_view(), name='recipient_list'),
    path('', MailingRecipientCreateView.as_view(), name='recipient_create'),
    path('', MailingRecipientDetailView.as_view(), name='recipient_detail'),
    path('', MailingRecipientDeleteView.as_view(), name='recipient_delete'),
    path('', MailingRecipientUpdateView.as_view(), name='recipient_update'),
]