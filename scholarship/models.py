from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
     pass

class Scholarship(models.Model):
    scholarship = models.TextField()
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="scholarships")
    date = models.DateField()
    amount = models.TextField(default=0)
    requirements = models.TextField(default="None")
    category = models.CharField(max_length=64, default="None")
    recieved= models.BooleanField(null=True)
    documents = models.JSONField(default=list, blank=True)
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "scholarship": self.scholarship,
            "requirements": self.requirements,
            "amount": self.amount,
            "url": self.url,
            "date": self.date,
            "category": self.category,
            "recieved": self.recieved,
            "documents": self.documents
            
        }
    def __str__(self):
        return f"{self.scholarship} [{self.date}]"

