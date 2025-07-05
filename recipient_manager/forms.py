from django import forms

from .models import MailingRecipient


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['email', 'fio', 'comment']
