from mailing.apps import MailingConfig
from .views import (MailingCreateView, MailingDeleteView, MailingDetailView, MailingUpdateView, MailingListView,
                    MailingSendView, AttemptMailingDetailView, MailingStatisticsView, AttemptMailingView, BlockingMailingView)
from django.urls import path, include


app_name = MailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/send/', MailingSendView.as_view(), name='send'),
    path('attempts/<int:mailing_id>', AttemptMailingView.as_view(), name='attempt_list'),
    path('attempts/<int:pk>/', AttemptMailingDetailView.as_view(), name='attempt_detail'),
    path('statistics/', MailingStatisticsView.as_view(), name='user_statistics'),
    path('<int:pk>/blocking/', BlockingMailingView.as_view(), name='blocking_mailing'),

]