import uuid

from django.shortcuts import render
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, FormView, UpdateView, ListView, DetailView
from .forms import UserRegisterForm, PasswordResetForm, PasswordResetRequestForm, BlockingUser
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from django.core.exceptions import ValidationError

from .models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('recipient:home')

    def form_valid(self, form):
        cache.delete('product_list')
        return super().form_valid(form)


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.confirmation_token = str(uuid.uuid4())
        user.save()
        self.send_confirmation_email(user.email, user.confirmation_token)
        return super().form_valid(form)

    def send_confirmation_email(self, user_email, token):

        subject = 'Подтверждение регистрации'
        message = f'Для подтверждения регистрации перейдите по ссылке: http://example.com/confirm/{token}'

        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class ConfirmRegistrationView(View):

    def get(self, request, token):
        try:
            user = User.objects.get(confirmation_token=token)
            user.is_confirmed = True
            user.is_active = True
            user.save()
            return redirect('users:login')
        except User.DoesNotExist:
            return redirect('users:register')


def custom_logout(request):
    logout(request)
    return redirect('/')


class PasswordResetRequestView(FormView):
    form_class = PasswordResetRequestForm
    template_name = 'users/password_reset_request.html'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_user_model().objects.filter(email=email).first()
        if user:
            user.password_reset_token = str(uuid.uuid4())
            user.save()
            self.send_password_reset_email(user.email, user.password_reset_token)
        return super().form_valid(form)

    def send_password_reset_email(self, user_email, token):
        subject = 'Восстановление пароля'
        message = f'Для восстановления пароля перейдите по ссылке: http://example.com/reset/{token}'
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def dispatch(self, request, *args, **kwargs):

        self.token = kwargs['token']
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = get_user_model().objects.filter(password_reset_token=self.token).first()
        if user:
            user.set_password(form.cleaned_data['password'])
            user.password_reset_token = None
            user.save()
            return super().form_valid(form)
        else:
            raise ValidationError('Недействительный токен восстановления пароля')


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    permission_required = 'users.view_user'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('users.list_user'):
            raise PermissionDenied


class UsersDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'users/users_detail.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'
    permission_required = 'users.list_user'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('users.list_user'):
            raise PermissionDenied


class BlockingUsersView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = BlockingUser
    template_name = 'users/user_block_form.html'
    success_url = reverse_lazy('users:users_list')
    permission_required = 'users.blocking_user'

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm('users.blocking_user'):
            raise PermissionDenied
        else:
            return BlockingUser