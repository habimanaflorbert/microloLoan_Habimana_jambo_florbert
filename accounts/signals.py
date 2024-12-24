from datetime import timezone,datetime
from django.dispatch import Signal
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete


# email verification
verification_email_signal = Signal()
