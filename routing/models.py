from django.db import models


class RouteCache(models.Model):

    origin = models.CharField(
        max_length=255
    )

    destination = (
        models.CharField(
            max_length=255
        )
    )

    distance_miles = (
        models.FloatField()
    )

    geometry = (
        models.JSONField()
    )

    created_at = (
        models.DateTimeField(
            auto_now_add=True
        )
    )

    class Meta:

        indexes = [
            models.Index(
                fields=[
                    "origin",
                    "destination",
                ]
            )
        ]