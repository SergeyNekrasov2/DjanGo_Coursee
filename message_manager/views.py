from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, TemplateView, CreateView,  DeleteView, UpdateView, View
from .forms import MessageForm
from .models import Message
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_manager/message_form.html'
    success_url = reverse_lazy('message_manager:messages_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    template_name = 'message_manager/messages_list.html'
    context_object_name = 'messages'
    permission_required = 'message_manager.view_message'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('message_manager.view_message') or not user == self.object.owner:
            raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    template_name = 'message_manager/message_detail.html'
    context_object_name = 'message'
    pk_url_kwarg = 'pk'
    permission_required = 'message_manager.view_message'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('message_manager.view_message') or not user == self.object.owner:
            raise PermissionDenied


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_manager/message_form.html'
    success_url = reverse_lazy('message_manager:messages_list')
    permission_required = 'message_manager.change_message'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('message_manager.change_message') or not user == self.object.owner:
            raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Message
    template_name = 'message_manager/message_delete.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('recipient_manager:home')
    permission_required = 'message_manager.delete_message'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('message_manager.delete_message') or not user == self.object.owner:
            raise PermissionDenied
