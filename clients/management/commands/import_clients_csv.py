import csv
from django.core.management.base import BaseCommand, CommandError
from clients.models import Client


class Command(BaseCommand):
    help = 'Загрузка клиентов из csv файла'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Загрузка клиентов'))

        with open('data/clients.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Client.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS('Клиенты загружены'))
