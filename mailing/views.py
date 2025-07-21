from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import MailingForm, BlockingMailing
from .models import Mailing, AttemptMailing
from django.http import HttpResponse
from django.core.management import call_command
from django.db.models import Count, Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class MailingCreateView(LoginRequiredMixin, CreateView):

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.status = 'Create'
        form.instance.mailing_owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    permission_required = 'mailing.view_mailing'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('mailing.view_mailing') or not user == self.object.owner:
            raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'
    pk_url_kwarg = 'pk'
    permission_required = 'mailing.view_mailing'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('mailing.view_mailing') or not user == self.object.owner:
            raise PermissionDenied


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.change_mailing'


    def has_permission(self):
        self.object = self.get_object()
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if not user.has_perm('mailing.change_mailing') or not user == self.object.mailing_owner:
            raise PermissionDenied


class BlockingMailingView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = BlockingMailing
    template_name = 'mailing/mailing_block_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.block_mailing'

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('mailing.block_mailing'):
            return BlockingMailing
        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.delete_mailing'

    def has_permission(self):
        self.object = self.get_object()
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if not user.has_perm('mailing.delete_mailing') or not user == self.object.mailing_owner:
            raise PermissionDenied


class MailingSendView(LoginRequiredMixin, DetailView):
    model = Mailing
    pk_url_kwarg = 'pk'
    template_name = 'mailing/mailing_send.html'

    def get(self, request, *args, **kwargs):
        mailing = self.get_object()
        return render(request, self.template_name, {'mailing': mailing})

    def save_attempt(self, mailing, status, status_response=None, recipient=None):
        attempt = AttemptMailing(mailing=mailing, attempt_date=timezone.now(), status=status)

        if recipient:
            attempt.status_response.append(f'{recipient} {status_response}')

        elif status_response:
            attempt.status_response = status_response

        attempt.save()

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()

        try:
            call_command('send_mailing', mailing.pk)
            return HttpResponse('Рассылка успешно отправлена', status=200)

        except Exception as e:

            self.save_attempt(mailing, 'Unsuccessful', e)
            return HttpResponse('Ошибка при отправке рассылки', status=500)


class AttemptMailingView(LoginRequiredMixin, View):
    template_name = 'attempt/attempt_mg_list.html'

    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        attempts = AttemptMailing.objects.filter(mailing=mailing)

        context = {
            'mailing': mailing,
            'attempts': attempts,
        }
        return render(request, self.template_name, context)


class AttemptMailingListView(LoginRequiredMixin, ListView):
    model = AttemptMailing
    template_name = 'attempt/attempt_list.html'
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = self.mailing
        return context


class AttemptMailingDetailView(LoginRequiredMixin, DetailView):
    model = AttemptMailing
    template_name = 'attempt/attempt_detail.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'pk'


class MailingStatisticsView(LoginRequiredMixin, View):
    template_name = 'mailing/user_statistics.html'

    def get_mailing_statistics(self, user):

        mailings = Mailing.objects.filter(mailing_owner=user)
        statistics = mailings.annotate(
            successful_attempts=Count('attemptmailing', filter=Q(attemptmailing__status='Successful')),
            unsuccessful_attempts=Count('attemptmailing', filter=Q(attemptmailing__status='Unsuccessful')),
            total_messages=Count('recipient')
        )
        result = []
        for mailing in statistics:
            result.append({
                'mailing_id': mailing.id,
                'date_first_sending': mailing.date_first_sending,
                'successful_attempts': mailing.successful_attempts,
                'unsuccessful_attempts': mailing.unsuccessful_attempts,
                'total_messages': mailing.total_messages,
            })
        return result

    def get_user_mailing_summary(self, user):

        attempts = AttemptMailing.objects.filter(mailing__mailing_owner=user)
        summary = attempts.aggregate(
            total_successful=Count('id', filter=Q(status='Successful')),
            total_unsuccessful=Count('id', filter=Q(status='Unsuccessful')),
            total_messages=Count('mailing__recipient', distinct=True)
        )
        return summary

    def get(self, request):
        user = request.user

        mailing_stats = self.get_mailing_statistics(user)

        user_summary = self.get_user_mailing_summary(user)

        context = {
            'mailing_stats': mailing_stats,
            'user_summary': user_summary,
        }

        return render(request, self.template_name, context)