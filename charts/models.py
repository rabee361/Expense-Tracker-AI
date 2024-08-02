from django.db import models
from accounts.models import Account
from django.core.validators import MinValueValidator
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db.models import Q  ,Sum


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='images/icons/categories',null=True)

    def __str__(self) -> str:
        return self.name



class ExpenseSubCategory(models.Model):
    category = models.ForeignKey(ExpenseCategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='images/icons/subctegories',null=True)

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
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
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

    @property
    def current_spending(self):
        accounts = Account.objects.filter(user=self.user).values_list('id')
        items = Item.objects.filter(Q(account__in=accounts) & Q(created__lte=self.end_date) & Q(created__gte=self.start_date) & Q(subcategory__category__name=self.category.name)).aggregate(total=Sum('price'))['total']
        if items :
            return items
        else:
            return 0

    # class Meta:
    #     unique_together = ['user', 'category','start_date','end_date']

    def __str__(self) -> str:
        return f'{self.user} - {self.category} - {self.limit} {self.currency}'
