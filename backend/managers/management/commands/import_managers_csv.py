import csv
from django.core.management.base import BaseCommand, CommandError
from managers.models import Manager


class Command(BaseCommand):
    help = "Загрузка менеджеров из csv файла"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Загрузка менеджеров"))

        with open("data/managers.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["first_name"] = row["first_name"].strip()
                row["last_name"] = row["last_name"].strip()

                manager, _ = Manager.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS("Менеджеры загружены"))
