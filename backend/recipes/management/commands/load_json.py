import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with open(
                    '../data/ingredients.json',
                    mode='r',
                    encoding='utf-8',
            ) as file:
                data = json.load(file)
                Ingredient.objects.bulk_create([Ingredient(**d) for d in
                                               data], ignore_conflicts=True)
        except Exception as error:
            self.stdout.write(f'{error}')
