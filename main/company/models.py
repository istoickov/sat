from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    number_of_employees = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_companies")

    def __str__(self):
        return str(self.company_name)
