import csv
from django.core.management.base import BaseCommand, CommandError
from clients.models import Client, Address


class Command(BaseCommand):
    help = 'Загрузка клиентов из csv файла'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Загрузка клиентов'))

        with open('data/clients.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['address'] = row['address'].strip()
                row['name'] = row['name'].strip()

                client, _ = Client.objects.get_or_create(**{'name': row['name']})

                if Address.objects.filter(street=row['address']).exists():
                    address = Address.objects.get(street=row['address'])
                else:
                    address, _ = Address.objects.get_or_create(**{'street': row['address'], 'lat': row['lat'], 'lon': row['lon']})

                client.addresses.add(address)
                client.save()

        self.stdout.write(self.style.SUCCESS('Клиенты загружены'))
