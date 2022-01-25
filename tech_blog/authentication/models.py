from django.db import models

# Create your models here.


class AuthenticationKeys(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    key = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'authentication_keys'

    def __str__(self):
        return str(self.name)


class AuthPermissions(models.Model):
    class_name = models.CharField(max_length=50, null=True, blank=True)
    url = models.TextField(max_length=100, null=True, blank=True)
    method = models.CharField(max_length=20, null=True, blank=True)
    platform_permissions = models.ForeignKey(AuthenticationKeys, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'auth_platform_permissions'

    def __str__(self):
        return str(self.url)
