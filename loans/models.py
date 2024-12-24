import uuid
from django.db import models
from accounts.models import User
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.


class Loan(models.Model):
    
    P="PENDING"
    A="APPROVED"
    D="DECLINED"
    
    STATUS_TYPE = (
        (A,"approved"),
        (P,"pending"),
        (D,"declined"),
    )
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user=models.ForeignKey(User,related_name='loan_user',on_delete=models.CASCADE)
    amount=models.IntegerField(max_length=7, null=False,blank=False)
    monthly_income=models.IntegerField(max_length=7, null=False,blank=False)
    status = models.CharField(
        _("status"), choices=STATUS_TYPE, max_length=50, default=P
    )
    updated_at = models.DateTimeField(_("updated at"), auto_now_add=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Loan")
        verbose_name_plural = _("Loans")
        ordering = ('amount',)
    
    def __str__(self):
            return self.user.first_name
    
    def get_absolute_url(self):
        return reverse("loans_detail", kwargs={"pk": self.pk})

