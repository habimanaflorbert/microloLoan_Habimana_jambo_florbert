from datetime import datetime, timezone
import uuid

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models
from django.utils.translation import gettext as _
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.urls import reverse
from django.utils.html import format_html


class UserManager(BaseUserManager):
 
    def create_user(self, telephone, first_name,last_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
    
        user = self.model(           
            telephone=telephone,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(
        self,  telephone, first_name,last_name, password=None, **extra_fields
    ):
        """
        Creates and saves a admin with the given email and password.
        """
        user = self.create_user(
          
            telephone=telephone,
            first_name=first_name,
            last_name=last_name,
            user_type=User.ADMIN,
            password=password,
            **extra_fields,
        )
        
        user.is_staff=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    ADMIN="ADMIN"
    END_USER="END_USER"
  
    
    
    USER_TYPE_CHOICE = (
        (ADMIN,"Admin"),
        (END_USER,"End user"),
       
    )
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name=models.CharField(_("first name"), max_length=100)
    last_name=models.CharField(_("last name"), max_length=100)
    telephone = models.CharField(
        _("telephone"), max_length=255,unique=True,validators=[
            MinLengthValidator(limit_value=13),
            MaxLengthValidator(limit_value=13)
        ]
    )

    user_type = models.CharField(
        _("user type"), choices=USER_TYPE_CHOICE, max_length=50)
    
    is_active = models.BooleanField(_("is active"), default=True)
    is_staff = models.BooleanField(_("is active"), default=False)
    
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = _("telephone")
    REQUIRED_FIELDS = ["first_name","last_name"]

    def get_full_name(self):
        # The user is identified by their address
        return self.first_name+' '+self.last_name


    def __str__(self):  # __unicode__ on Python 2O
        return self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

