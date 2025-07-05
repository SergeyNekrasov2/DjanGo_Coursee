from django.contrib import admin

from mailing.models import Mailing, AttemptMailing

admin.site.register(Mailing)
admin.site.register(AttemptMailing)
