from django.shortcuts import render
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import PurchaseCreateForm, IngredientUpdateForm, MenuItemCreateForm, RecipeRequirementCreateForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
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

    def get_initial(self): 
        initial_base= super(POSCreateView, self).get_initial()
        initial_base['item'] = MenuItem.objects.get(id=self.kwargs['pk'])
        return initial_base

    #now it works, but i don't really understand it. figure it out, deirdre!
    def post(self, request, pk):
         menu_item_id = request.POST["item"]
         menu_item = MenuItem.objects.get(pk=menu_item_id)
         requirements = menu_item.reciperequirement_set
         purchase = Purchase(item=menu_item)
         #ingredient count check -- could this be more efficient? 1 for loop not 2?
         for requirement in requirements.all():
             required_ingredient = requirement.ingredient
             if required_ingredient.quantity >= requirement.quantity:
                continue
             else:
                 messages.error(request, "Insufficient Ingredients")
                 return redirect("posindex")
         #ingredient decrement
         for requirement in requirements.all():
             required_ingredient = requirement.ingredient
             required_ingredient.quantity -= requirement.quantity
             required_ingredient.save() 
            
         purchase.save()
         messages.success(request, "Purchase Made!")
         return redirect("posindex")

class PurchaseListView(ListView):
    model = Purchase
    queryset = Purchase.objects.all().order_by("-timestamp")
    template_name = "inventory/purchaseindex.html"
    context_object_name = 'purchase_list'

class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseCreateForm
    template_name = "inventory/updatepurchase.html"
    success_message = "Purchase Updated!"
    success_url = reverse_lazy("purchaseindex")

class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = "inventory/deletepurchase.html"
    success_message = "Purchase Deleted!"
    success_url = reverse_lazy("purchaseindex")

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

class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_message = "Ingredient Deleted!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/deleteingredient.html"

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

    def get_context_data(self, **kwargs):
        kwargs['pk'] = self.kwargs['pk']
        return super(RecipeRequirementCreateView, self).get_context_data(**kwargs)

    def get_initial(self):
        initial_base = super(RecipeRequirementCreateView, self).get_initial()
        initial_base['menu_item'] = MenuItem.objects.get(id=self.kwargs['pk'])
        return initial_base

class RecipeRequirementUpdateView(UpdateView):
    model = RecipeRequirement
    form_class = RecipeRequirementCreateForm
    success_message = "Recipe Requirement Updated!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/updatereciperequirement.html"

class RecipeRequirementDeleteView(DeleteView):
    model = RecipeRequirement
    success_message = "Recipe Requirement Deleted!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/deletereciperequirement.html"