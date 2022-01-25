from django.db import models
from myUsers.models import CustomUser
from queries.models import Queries
# Create your models here.


def nameFile(instance, filename):
    print("instance: ", instance)
    return '/'.join(['responses', str(instance), filename])


class Responses(models.Model):
    u_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    q_id = models.ForeignKey(Queries, related_name="responses", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    file_path = models.FileField(upload_to=nameFile, blank=True)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.u_id)
