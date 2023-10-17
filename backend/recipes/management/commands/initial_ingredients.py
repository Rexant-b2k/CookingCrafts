import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def _create_data(self):
        with open("fixtures/ingredients.json") as inp_file:
            data_array = json.load(inp_file)
            counter = 0
            for line in data_array:
                name = line['name']
                unit = line['measurement_unit']
                if Ingredient.objects.filter(
                    name=name, measurement_unit=unit
                ).exists():
                    continue
                Ingredient.objects.create(name=name, measurement_unit=unit)
                counter += 1
        print('Added new ingredients to database: ', counter)

    def handle(self, *args, **options):
        self._create_data()
