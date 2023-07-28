from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment, Availability


@receiver(post_save, sender=Appointment)
def update_availability(sender, instance, created, **kwargs):
    if created:
        availability = Availability.objects.get(time=instance.start_time)
        instance.advisor.availability.remove(availability)