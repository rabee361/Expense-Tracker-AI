from django.db import models
from accounts.models import Account
from django.core.validators import MinValueValidator
from accounts.models import CustomUser
from django.core.exceptions import ValidationError


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name



class ExpenseSubCategory(models.Model):
    category = models.ForeignKey(ExpenseCategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name



class Item(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    item_name = models.CharField(max_length = 100)
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    subcategory = models.ForeignKey(ExpenseSubCategory,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.item_name
    


class UpcomingPayment(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    subcategory = models.ForeignKey(ExpenseSubCategory,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.name
    



class SavingsGoal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , unique=True)
    budget = models.IntegerField(validators=[MinValueValidator(1000)])
    current = models.IntegerField(validators=[MinValueValidator(1000)],default=0)
    date = models.DateField()
    notes = models.CharField(max_length=200 , null=True, blank=True)
    currency = models.CharField(max_length=100,default='ل.س')

    def add_payment(self,payment):
        if (self.current + payment) < self.budget:
            self.current += payment
            self.save()
        
    def __str__(self) -> str:
        return self.name
    



# check the limit by checking the sum of all the spendings in that category

class SpendingLimit(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    limit = models.IntegerField(validators=[MinValueValidator(1000)])
    category = models.ForeignKey(ExpenseCategory , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    currency = models.CharField(max_length=100,default='ل.س')

    def __str__(self) -> str:
        return f'{self.user} - {self.category} - {self.limit} {self.currency}'
