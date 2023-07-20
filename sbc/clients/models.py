from django.db import models
from django.urls import reverse


class Stage(models.Model):

    TYPE_STAGES = (
        ('Unknown', 'unknown'),
        ('Accept', 'accept'),
        ('Refuse', 'refuse'),
        ('Onhold', 'onhold'),
    )

    type = models.CharField(choices=TYPE_STAGES, default='Unknown')

    def __str__(self):
        return f'{self.type}'



# Create your models here.
class Citizen(models.Model):

    firstname = models.CharField(max_length=100, blank=False, null=False)
    lastname = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=False, null=False)
    telephone_num = models.CharField(max_length=13, blank=False, null=True)
    age = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, default=16)


    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.is_active}'


    def get_absolute_url(self):
        return reverse("clients:citizen-detail", kwargs={"id": self.id})




