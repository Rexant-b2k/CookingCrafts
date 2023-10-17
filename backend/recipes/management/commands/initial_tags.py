# flake8: noqa
from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    TAGS = [
        {'name': 'Breakfast',
         'color': '#88b04b',
         'slug': 'breakfast'},
        {'name': 'Dinner',
         'color': '#0f4c81',
         'slug': 'dinner'},
        {'name': 'Supper',
         'color': '#5f4b8b',
         'slug': 'supper'},  
    ]

    def _create_data(self):
        counter = 0
        for entry in self.TAGS:
            name = entry['name']
            color = entry['color']
            slug = entry['slug']
            if Tag.objects.filter(name=name).exists():
                continue
            Tag.objects.create(name=name, color=color, slug=slug)
            counter += 1
        print('Added new Tags to database: ', counter)

    def handle(self, *args, **options):
        self._create_data()
