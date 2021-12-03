from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement, RevenueDay
from .forms import PurchaseCreateForm, IngredientUpdateForm, MenuItemCreateForm, RecipeRequirementCreateForm, RevenueDayCreateForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect("accounts/login/")

@login_required
def homepage(request):
    context = {
        'revenue' : RevenueDay.objects.all().last(),
        'ingredient_list' : Ingredient.objects.all,
        'profit' : RevenueDay.objects.all().last().amount - RevenueDay.objects.all().last().cost
    }
    return render(request, "inventory/home.html", context)

class NewUserView(LoginRequiredMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "inventory/createnewuser.html"
    
class RevenueDayCreateView(LoginRequiredMixin, CreateView):
    model = RevenueDay
    form_class = RevenueDayCreateForm
    template_name = "inventory/createrevenueday.html"
    success_message = "New Day Started!"
    success_url = reverse_lazy("home")

class RevenueDayListView(LoginRequiredMixin, ListView):
    model = RevenueDay
    template_name = "inventory/revenuedayindex.html"
    queryset = RevenueDay.objects.all().order_by("-day")

    def get_context_data(self, **kwargs):
        context = super(RevenueDayListView, self).get_context_data(**kwargs)
        context.update({
            'current': RevenueDay.objects.all().last(),
        })
        return context

class RevenueDayUpdateView(LoginRequiredMixin, UpdateView):
    model = RevenueDay
    form_class = RevenueDayCreateForm
    template_name = "inventory/updaterevenueday.html"
    success_message = "Day Updated!"
    success_url = reverse_lazy("revenuedayindex")

class RevenueDayDeleteView(LoginRequiredMixin, DeleteView):
    model = RevenueDay
    template_name = "inventory/deleterevenueday.html"
    success_message = "Day Deleted!"
    success_url = reverse_lazy("revenuedayindex")

class PurchasesByDayView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchasesbyday.html"

    def get_context_data(self, **kwargs):
        context = super(PurchasesByDayView, self).get_context_data(**kwargs)
        context.update({
            'purchases': Purchase.objects.filter(day__pk=self.kwargs['pk']),
            'time': RevenueDay.objects.get(id=self.kwargs['pk']),
        })
        return context

class POSListView(LoginRequiredMixin, ListView):
    model = MenuItem
    queryset = MenuItem.objects.all().order_by("name")
    template_name = "inventory/posindex.html"
    #extra_context={'revenue': RevenueDay.objects.all().last(),}

    def get_context_data(self, **kwargs):
        context = super(POSListView, self).get_context_data(**kwargs)
        context.update({
            'revenue': RevenueDay.objects.all().last(),
        })
        return context

class POSCreateView(LoginRequiredMixin, CreateView):
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
         day = RevenueDay.objects.all().last()
         #ingredient count check -- could this be more efficient? 1 for loop not 2?
         for requirement in requirements.all():
             required_ingredient = requirement.ingredient
             if required_ingredient.quantity >= requirement.quantity:
                continue
             else:
                 messages.error(request, "Insufficient Ingredients")
                 return redirect("posindex")
         #ingredient decrement and cost addition
         for requirement in requirements.all():
             required_ingredient = requirement.ingredient
             required_ingredient.quantity -= requirement.quantity
             day.cost += (required_ingredient.price * requirement.quantity) #price per unit * the number needed
             required_ingredient.save()
         #daily revenue increment
         day.amount += menu_item.price   
         purchase.save()
         day.save()
         messages.success(request, "Purchase Made!")
         return redirect("posindex")

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    queryset = Purchase.objects.all().order_by("-timestamp")
    template_name = "inventory/purchaseindex.html"
    context_object_name = 'purchase_list'

class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Purchase
    form_class = PurchaseCreateForm
    template_name = "inventory/updatepurchase.html"
    success_message = "Purchase Updated!"
    success_url = reverse_lazy("purchaseindex")

class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "inventory/deletepurchase.html"
    success_message = "Purchase Deleted!"
    success_url = reverse_lazy("purchaseindex")

    #need to find the request.post that will make this work
    def delete(self, request, pk):
        purchase_id = pk
        purchase = Purchase.objects.get(pk=purchase_id)
        menu_item = purchase.item
        requirements = menu_item.reciperequirement_set
        day = purchase.day

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity += requirement.quantity
            required_ingredient.save()
        
        day.amount -= menu_item.price
        day.save()
        purchase.delete()
        return redirect("purchaseindex")


class InventoryListView(LoginRequiredMixin, ListView):
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

class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientUpdateForm
    success_message = "Ingredient updated!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/updateingredient.html"

class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientUpdateForm
    success_message = "Ingredient Created!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/createingredient.html"

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_message = "Ingredient Deleted!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/deleteingredient.html"

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    success_message = "Menu Item Updated!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/updatemenuitem.html"

    def get_context_data(self, **kwargs):
        kwargs['recipe_requirement_list'] = RecipeRequirement.objects.filter(menu_item__pk=self.kwargs['pk']).order_by('ingredient')
        kwargs['pk'] = self.kwargs['pk']
        return super(MenuItemUpdateView, self).get_context_data(**kwargs)

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    success_message = "Menu Item Created!"
    success_url = reverse_lazy("inventoryindex")
    template_name = "inventory/createmenuitem.html"

class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementCreateForm
    success_message = "Recipe Requirement Created!"
    template_name = "inventory/createreciperequirement.html"

    def get_success_url(self):
        return reverse('menuitemupdate', args=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        kwargs['pk'] = self.kwargs['pk']
        return super(RecipeRequirementCreateView, self).get_context_data(**kwargs)

    def get_initial(self):
        initial_base = super(RecipeRequirementCreateView, self).get_initial()
        initial_base['menu_item'] = MenuItem.objects.get(id=self.kwargs['pk'])
        return initial_base

class RecipeRequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = RecipeRequirement
    form_class = RecipeRequirementCreateForm
    success_message = "Recipe Requirement Updated!"
    template_name = "inventory/updatereciperequirement.html"
    
    def get_success_url(self):
        return reverse('menuitemupdate', args=self.kwargs['id'])

class RecipeRequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    success_message = "Recipe Requirement Deleted!"
    template_name = "inventory/deletereciperequirement.html"

    def get_success_url(self):
        return reverse('menuitemupdate', args=self.kwargs['id'])