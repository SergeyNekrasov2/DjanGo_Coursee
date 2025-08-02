from django.db import models


from users.models import User


class MailingRecipient(models.Model):

    email = models.EmailField(unique=True, verbose_name='Email')
    fio = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(blank=True, null=True)
    recipient_owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец карточки клиента', blank=True, null=True)

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'


    def __str__(self):
        return self.email