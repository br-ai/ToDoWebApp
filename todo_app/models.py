from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

# this function will return one week away time
def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class Todo(models.Model):
    
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # due_date = models.DateTimeField(null=True, blank=True)
    etat = models.BooleanField(default=False)
    heure_de_fin = models.CharField(max_length=100, null = True, blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.description}"
    