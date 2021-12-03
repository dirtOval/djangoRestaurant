from django import forms
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement, RevenueDay

class PurchaseCreateForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = ('item', 'timestamp', 'day')
        item = forms.ModelChoiceField(queryset=MenuItem.objects.all())
        timestamp = forms.DateTimeField()
        day = forms.ModelChoiceField(queryset=RevenueDay.objects.all())

        def __init__(self, *args, **kwargs):
            latest = RevenueDay.objects.latest('day')
            latest.__repr__()
            self.fields['day'].initial = latest.pk
            super(PurchaseCreateForm, self).__init__(*args, **kwargs)


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

class RevenueDayCreateForm(forms.ModelForm):
    class Meta:
        model = RevenueDay
        fields = "__all__"
        