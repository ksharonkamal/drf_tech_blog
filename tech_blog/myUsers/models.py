from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# from django.utils.translation import ugettext_lazy as _
# from .validators import DomainUnicodeusernameValidator,DomainUnicodenameValidator,DomainUnicodemobileValidator
from .managers import CustomUserManager
from django.utils import timezone
# Create your models here.
from django.utils.translation import gettext_lazy
from technology.models import Technology


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    firstname = models.CharField(max_length=40, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True, null=True)
    technology = models.ManyToManyField(Technology)
    # technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    password = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'firstname', 'lastname', 'mobile']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None): return self.is_superuser
    def has_module_perms(self, app_label): return True
