from django.db import models
from django.urls import reverse


class Flats(models.Model):
    link = models.CharField(unique=True, max_length=300)
    reference = models.CharField(max_length=30, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    price_meter = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=3000, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    photo_links = models.TextField(blank=True, null=True)
    is_tg_posted = models.BooleanField(blank=True, null=True)
    is_archive = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flats'

    
class Cities(models.Model):
    city = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'cities'

    def get_absolute_url(self):
        return reverse("filter_city", kwargs={"sort_city": self.city})
    

class UserSubscriptions(models.Model):
    user_id = models.BigIntegerField(unique=True)
    sort_price = models.BooleanField(blank=True, null=True)
    sort_city = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_subscriptions'
