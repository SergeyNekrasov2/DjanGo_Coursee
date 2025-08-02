from django.db import models

from users.models import User


class Message(models.Model):

    subject = models.CharField(max_length=50, verbose_name='Тема сообщения')
    body_text = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец рассылки', blank=True, null=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

