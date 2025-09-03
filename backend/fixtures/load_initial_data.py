import json
import os
from recipes.models import Ingredient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'ingredients.json'), encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    Ingredient.objects.update_or_create(
        name=item['name'],
        defaults={'measurement_unit': item['measurement_unit']}
    )
