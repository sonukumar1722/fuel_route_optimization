import csv

from django.core.management.base import (
    BaseCommand,
)

from django.contrib.gis.geos import (
    Point,
)

from fuel.models import (
    FuelStation,
)

from services.providers.openroute_service import (
    OpenRouteServiceProvider,
)


class Command(BaseCommand):

    help = (
        "Import fuel stations"
    )

    def add_arguments(
        self,
        parser,
    ):

        parser.add_argument(
            "--csv",
            required=True,
        )

    def handle(
        self,
        *args,
        **options,
    ):

        provider = (
            OpenRouteServiceProvider()
        )

        csv_file = (
            options["csv"]
        )

        with open(
            csv_file,
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(
                file
            )

            imported = 0
            skipped = 0

            for row in reader:

                address = (
                    f"{row['Address']}, "
                    f"{row['City']}, "
                    f"{row['State']}"
                )

                existing = (
                    FuelStation.objects
                    .filter(
                        address=row[
                            "Address"
                        ]
                    )
                    .first()
                )

                if existing:

                    existing.fuel_price = (
                        row[
                            "Retail Price"
                        ]
                    )

                    existing.save()

                    continue

                try:
                    result = provider.geocode(
                        address
                    )
                    if not result:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Could not geocode: {address}"
                                )
                            )
                        continue

                    lat, lon = result

                    imported += 1

                except Exception as exc:

                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping: {address}"
                        )
                    )

                    skipped += 1
                    continue

                FuelStation.objects.create(
                    name=row[
                        "Truckstop Name"
                    ],
                    address=row[
                        "Address"
                    ],
                    city=row["City"],
                    state=row["State"],
                    fuel_price=row[
                        "Retail Price"
                    ],
                    location=Point(
                        lon,
                        lat,
                        srid=4326,
                    ),
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Imported={imported}, Skipped={skipped} - {row['Truckstop Name']}"
                    )
                )

