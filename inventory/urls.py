from django.urls import path, include

from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path("", views.homepage, name="home"),
    path("logout", views.logout_view, name="logout"),
    path("newuser", views.NewUserView.as_view(), name="newuser"),
    path("day/create", views.RevenueDayCreateView.as_view(), name="daycreate"),
    path("day/index", views.RevenueDayListView.as_view(), name="revenuedayindex" ),
    path("day/<pk>", views.PurchasesByDayView.as_view(), name="purchasesbyday"),
    path("day/<pk>/update/", views.RevenueDayUpdateView.as_view(), name="revenuedayupdate"),
    path("day/<pk>/delete/", views.RevenueDayDeleteView.as_view(), name="revenuedaydelete"),
    path("pos/", views.POSListView.as_view(), name="posindex"),
    path("pos/purchase/index/", views.PurchaseListView.as_view(), name="purchaseindex"),
    path("pos/<pk>/purchase/", views.POSCreateView.as_view(), name="poscreatepurchase"),
    path("pos/purchase/<pk>/update/", views.PurchaseUpdateView.as_view(), name="purchaseupdate"),
    path("pos/purchase/<pk>/delete/", views.PurchaseDeleteView.as_view(), name="purchasedelete"),
    path("inventory/index/", views.InventoryListView.as_view(), name="inventoryindex"),
    path("inventory/ingredient/<pk>/update/", views.IngredientUpdateView.as_view(), name="ingredientupdate"),
    path("inventory/ingredient/create/", views.IngredientCreateView.as_view(), name="ingredientcreate"),
    path("inventory/ingredient/<pk>/delete/", views.IngredientDeleteView.as_view(), name="ingredientdelete"),
    path("inventory/menuitem/<pk>/update/", views.MenuItemUpdateView.as_view(), name="menuitemupdate"),
    path("inventory/menuitem/create/", views.MenuItemCreateView.as_view(), name="menuitemcreate"),
    path("inventory/menuitem/<pk>/requirement/create/", views.RecipeRequirementCreateView.as_view(), name="reciperequirementcreate"),
    path("inventory/menuitem/<id>/requirement/<pk>/update/", views.RecipeRequirementUpdateView.as_view(), name="reciperequirementupdate"),
    path("inventory/menuitem/<id>/requirement/<pk>/delete/", views.RecipeRequirementDeleteView.as_view(), name="reciperequirementdelete"),
]