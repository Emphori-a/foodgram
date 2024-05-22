import csv
import os

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.core.management.base import CommandParser

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Load data from a CSV file into the Ingredient table'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_name', type=str, help='Имя CSV файла')

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['file_name']),
                      mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены.'))
        except FileNotFoundError:
            raise CommandError(
                'Указанный файл должен находиться в директории data.'
            )
