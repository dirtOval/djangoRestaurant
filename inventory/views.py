from django.shortcuts import render
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import PurchaseCreateForm, IngredientUpdateForm, MenuItemCreateForm, RecipeRequirementCreateForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
# Create your views here.

revenue = 0

def homepage(request):
    context = {
        'revenue' : revenue
    }
    return render(request, "inventory/home.html", context)
    

class POSListView(ListView):
    model = MenuItem
    queryset = MenuItem.objects.all().order_by("name")
    template_name = "inventory/posindex.html"
    extra_context={'revenue': revenue}

class POSCreateView(CreateView):
    model = Purchase
    form_class = PurchaseCreateForm
    success_message = "Purchase completed!"
    success_url = reverse_lazy("posindex")
    template_name = "inventory/createpurchase.html"

class InventoryListView(ListView):
    model = Ingredient
    queryset = Ingredient.objects.all().order_by("name")
    template_name = "inventory/inventoryindex.html"
    context_object_name = 'ingredient_list'

    def get_context_data(self, **kwargs):
        context = super(InventoryListView, self).get_context_data(**kwargs)
        context.update({
            'menu_item_list': MenuItem.objects.order_by('name'),
        })
        return context

class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientUpdateForm
    success_message = "Ingredient updated!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/updateingredient.html"

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientUpdateForm
    success_message = "Ingredient Created!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/createingredient.html"

class MenuItemUpdateView(UpdateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    success_message = "Menu Item Updated!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/updatemenuitem.html"

    def get_context_data(self, **kwargs):
        kwargs['recipe_requirement_list'] = RecipeRequirement.objects.filter(menu_item__pk=self.kwargs['pk']).order_by('ingredient')
        kwargs['pk'] = self.kwargs['pk']
        return super(MenuItemUpdateView, self).get_context_data(**kwargs)

class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    success_message = "Menu Item Created!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/createmenuitem.html"

class RecipeRequirementCreateView(CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementCreateForm
    success_message = "Recipe Requirement Created!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/createreciperequirement.html"

class RecipeRequirementUpdateView(UpdateView):
    model = RecipeRequirement
    form_class = RecipeRequirementCreateForm
    success_message = "Recipe Requirement Updated!"
    success_url = reverse_lazy("menuitemupdate")
    template_name = "inventory/updatereciperequirement.html"