from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Create your models here.
class Coordinates(models.Model):
    user_id = models.IntegerField()
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    z_coordinate = models.FloatField()

    def __str__(self):
        return str(self.x_coordinate) + str(self.y_coordinate) + str(self.z_coordinate)


@receiver(post_save, sender=Coordinates)
def coordinate_post_save(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"con_{str(instance.user_id)}",
        {
            "type": "send_data",
            "data": {
                "success": True
            }
        }
    )
