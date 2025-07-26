from typing import Any
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.db import transaction

from clients.models import Client, MetaClient, Address


class Command(BaseCommand):
    help = "add new clients through CLI"

    def setup_select(self, options: QuerySet):
        self.stdout.write(self.style.NOTICE("[SELECT META_CLIENT]"))
        self.stdout.write("Please select one:")
        for i, o in enumerate(options, 1):
            self.stdout.write(f"{i}. " + str(o))

        return options[int(input("Select: ")) - 1]

    def setup_create_address(self) -> Address:
        self.stdout.write(self.style.NOTICE("[CREATING ADDRESS]"))
        street = input("Input street address: ")
        link = input("Input 2gis link: ")
        lat = float(input("Input latitude (широта): "))
        lon = float(input("Input longitude (долгота): "))
        return Address(street=street, twogis_link=link, lat=lat, lon=lon)

    def setup_create_shop(self) -> dict[str, Any]:
        meta_client: MetaClient = self.setup_select(MetaClient.objects.all())

        new_address = self.setup_create_address()
        new_address.save()

        self.stdout.write(self.style.NOTICE("[CREATING SHOP]"))
        shop_name = input("Input shop name: ")

        return {"meta_client": meta_client, "address": new_address, "name": shop_name}

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.NOTICE("[STARTING TRANSACTION]"))

            with transaction.atomic():
                new_client_data = self.setup_create_shop()

                self.stdout.write(self.style.NOTICE("[PREVIEW]"))
                for k, v in new_client_data.items():
                    self.stdout.write(self.style.NOTICE(k + " = ") + str(v))

                if input("Confirm (y/N): ").lower() == "y":
                    new_client = Client(**new_client_data)
                    new_client.save()

                    self.stdout.write(
                        self.style.SUCCESS(f"New client {new_client} was added!")
                    )

            self.stdout.write(self.style.NOTICE("[END TRANSACTION SUCCESSFULLY]"))
        except Exception as e:
            self.stdout.write(self.style.NOTICE("[END TRANSACTION FAILED]"))
            self.stderr.write(self.style.ERROR(f"Something went wrong: {e}"))
