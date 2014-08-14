from django.db import models
from django.contrib.auth.models import User


class Employer(models.Model):
    """
    A simple employer model
    """
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=60)
    company_description = models.TextField(blank=True)
    address = models.TextField()
    website = models.URLField(blank=True)

    class Meta:
        ordering = ('company_name',)

    def __unicode__(self):
        return self.company_name
