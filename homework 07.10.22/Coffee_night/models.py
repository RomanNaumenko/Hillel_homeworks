from django.db import models
from django.utils.translation import gettext_lazy as _


class Places(models.Model):
    name = models.CharField(max_length=50)


class Route(models.Model):
    start_point = models.IntegerField()
    stop_point = models.JSONField()
    destination_point = models.IntegerField()
    country = models.CharField(max_length=50)
    loc = models.CharField(max_length=50)  # Локація
    desc = models.TextField()  # Опис походу

    class Types(models.TextChoices):
        HIKING = 'HIKING', _('Hiking')
        MOUNTAIN_CLIMBING = 'MOUNTAIN_CLIMBING', _('Mountain climbing')
        SKIING = 'SKIING', _('Skiing')
        SNOWBOARDING = 'SNOWBOARDING', _('Snowboarding')
        CAMPING = 'CAMPING', _('Camping')
        FISHING = 'FISHING', _('Fishing')
        BIKING = 'BIKING', _('Biking')
        HUNTING = 'HUNTING', _('Hunting')
        PHOTOGRAPHY = 'PHOTOGRAPHY', _('Photography')
        OTHER = 'OTHER', _('Other')

    route_type = models.CharField(max_length=50, choices=Types.choices, default=Types.HIKING)  # Тип походу
    duration = models.IntegerField()  # Тривалість походу


class Event(models.Model):
    id_route = models.IntegerField()
    event_admin = models.IntegerField()
    approved_users = models.JSONField()
    pending_users = models.JSONField()
    start_data = models.DateField()
    price = models.IntegerField()


class Review(models.Model):
    id_route = models.IntegerField()
    text = models.TextField(max_length=500)
    rating = models.IntegerField()
