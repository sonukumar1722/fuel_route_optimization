from django.contrib.gis.db import models


class FuelStation(models.Model):

    name = models.CharField(
        max_length=255
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    fuel_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    location = models.PointField(
        geography=True
    )

    created_at = (
        models.DateTimeField(
            auto_now_add=True
        )
    )

    updated_at = (
        models.DateTimeField(
            auto_now=True
        )
    )

    class Meta:

        indexes = [
            models.Index(
                fields=["city"]
            ),
            models.Index(
                fields=["state"]
            ),
        ]

    def __str__(self):

        return (
            f"{self.name}"
            f" ({self.state})"
        )