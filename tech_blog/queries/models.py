from django.db import models
from myUsers.models import CustomUser
from technology.models import Technology
# Create your models here.


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.title), filename])


class Queries(models.Model):
    u_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    t_id = models.ForeignKey(Technology, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to=nameFile, blank=True)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)
