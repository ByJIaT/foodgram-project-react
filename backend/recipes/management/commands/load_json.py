import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

DATASET = {
    Ingredient: 'ingredients.json',
    Tag: 'tags.json',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            for model, file in DATASET.items():
                with open(
                        f'../data/{file}',
                        mode='r',
                        encoding='utf-8',
                ) as f:
                    data = json.load(f)
                    model.objects.bulk_create([model(**d) for d in data],
                                              ignore_conflicts=True)
        except Exception as error:
            self.stdout.write(f'{error}')
