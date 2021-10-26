from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("pos", views.POSListView.as_view(), name="posindex"),
    path("pos/<pk>/purchase", views.POSCreateView.as_view(), name="poscreatepurchase"),
    path("inventory/index", views.InventoryListView.as_view(), name="inventoryindex"),
    path("inventory/ingredient/<pk>/update", views.IngredientUpdateView.as_view(), name="ingredientupdate"),
    path("inventory/ingredient/create", views.IngredientCreateView.as_view(), name="ingredientcreate"),
    path("inventory/menuitem/<pk>/update", views.MenuItemUpdateView.as_view(), name="menuitemupdate"),
    path("inventory/menuitem/create", views.MenuItemCreateView.as_view(), name="menuitemcreate"),
    path("inventory/menuitem/<pk>/requirement/create", views.RecipeRequirementCreateView.as_view(), name="reciperequirementcreate"),
    path("inventory/menuitem/requirement/<pk>/update", views.RecipeRequirementUpdateView.as_view(), name="reciperequirementupdate")
]