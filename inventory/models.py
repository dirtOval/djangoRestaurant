from django.db import models
from django.utils import timezone

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.FloatField()
    max = models.FloatField(default=0)
    unit = models.CharField(max_length=15)
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ingredients"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Menu Items"

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return self.menu_item.name + self.ingredient.name

class Purchase(models.Model):
    item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item.name

class RevenueDay(models.Model):
    day = models.DateField(default=timezone.now)
    amount = models.FloatField()

    def __str__(self):
        return self.day

    #THIS DOES NOT WORK. need to fix this.
    # @classmethod
    # def create(cls, item, timestamp):
    #     purchase = cls(item=item, timestamp=timestamp)
    #     #need to get a make a list of recipe requirements and iterate thru each of them
    #     #to check if there are enough ingredients to make the sale
    #     requirements= RecipeRequirement.objects.filter(menu_item=item)
    #     for req in requirements:
    #         if req.ingredient.quantity >= req.quantity:
    #             continue
    #         else:
    #             print("insufficient ingredients to prepare recipe!")
    #             return None
    #     return purchase
    #do it in views, you nerd. don't need to do it here