from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from mailing.models import Mailing
from .forms import MailingRecipientForm
from .models import MailingRecipient
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, ListView, TemplateView, CreateView, DeleteView, UpdateView, View


class MailingRecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'recipient_manager/recipient_list.html'
    context_object_name = 'recipients'
    permission_required = 'recipient.view_recipient'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('recipient.view_recipient') or not user == self.object.owner:
            raise PermissionDenied


class MailingRecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = 'recipient_manager/recipient_detail.html'
    context_object_name = 'recipient'
    pk_url_kwarg = 'pk'
    permission_required = 'recipient.view_recipient'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('recipient.view_recipient') or not user == self.object.owner:
            raise PermissionDenied


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'recipient_manager/recipient_form.html'
    success_url = reverse_lazy('recipient_manager:recipient_list')

    def form_valid(self, form):
        form.instance.mailing_owner = self.request.user
        return super().form_valid(form)


class MailingRecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = MailingRecipient
    template_name = 'recipient_manager/recipients_delete.html'
    context_object_name = 'recipient'
    pk_url_kwarg = 'pk'
    permission_required = 'recipient.delete_recipient'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('recipient.delete_recipient') or not user == self.object.owner:
            raise PermissionDenied


class MailingRecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'recipient_manager/recipient_form.html'
    success_url = reverse_lazy('recipient_manager:recipient_list')
    permission_required = 'recipient.change_recipient'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('recipient.change_recipient') or not user == self.object.owner:
            raise PermissionDenied


class HomeView(TemplateView):
    template_name = 'recipient_manager/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['total_mailings'] = Mailing.objects.count()


        context['active_mailings'] = Mailing.objects.filter(status='Running').count()


        context['unique_recipients'] = MailingRecipient.objects.count()  # или оптимизированный запрос

        return context
