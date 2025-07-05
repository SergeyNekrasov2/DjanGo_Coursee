import datetime

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from mailing.models import Mailing, AttemptMailing


def save_attempt(mailing, status,  status_response=None, recipient=None):
    attempt = AttemptMailing(mailing=mailing, attempt_date=timezone.now(), status=status)

    if recipient:
        attempt.status_response.append(f'{recipient} {status_response}')

    elif status_response:
        attempt.status_response = status_response

    attempt.save()


class Command(BaseCommand):
    help = 'Отправляет выбранную рассылку вручную через командную строку'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки для отправки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена'))
            return

        mailing.status = "Running"

        if mailing.date_first_sending is None:
            mailing.date_first_sending = timezone.now().date()

        mailing.save()

        from_email = settings.EMAIL_HOST_USER
        recipients = list(mailing.recipient.all().values_list('email', flat=True))

        if not recipients:
            save_attempt(mailing, 'Unsuccessful', 'Нет получателей')
            self.stdout.write(self.style.ERROR('Нет получателей для отправки'))
            return

        # email_data = [
        #     (mailing.message.subject, mailing.message.body_text, from_email, [recipient])
        #     for recipient in recipients
        # ]

        try:
            for recipient in recipients:
                send_mail(mailing.message.subject, mailing.message.body_text, from_email, recipient.email)
                save_attempt(mailing, 'Unsuccessful', recipient=recipient.email)

            mailing.date_end_shipment = timezone.now().date()
            mailing.status = 'Completed'

            mailing.save()

            save_attempt(mailing, 'Completed')
            self.stdout.write(self.style.SUCCESS('Рассылка успешно отправлена'))

        except Exception as e:

            save_attempt(mailing, 'Unsuccessful', e)
            # self.stdout.write(self.style.ERROR(f'Ошибка при отправке рассылки: {str(e)}'))