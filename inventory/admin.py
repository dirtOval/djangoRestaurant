from django.contrib import admin

from inventory.models import RecipeRequirement
from .models import Ingredient, RecipeRequirement, MenuItem, Purchase
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(RecipeRequirement)
admin.site.register(MenuItem)
admin.site.register(Purchase)