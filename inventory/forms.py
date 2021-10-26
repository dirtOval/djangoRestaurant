from django import forms
from django import forms
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement

class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = "__all__"

class IngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"

class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"

class RecipeRequirementCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = "__all__"