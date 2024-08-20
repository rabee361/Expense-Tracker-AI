import random
from datetime import datetime, timedelta
import pytz
from django.core.management.base import BaseCommand
from charts.models import Item , ExpenseSubCategory
from accounts.models import Account

class Command(BaseCommand):
    help = "populate DB with Data"
    def add_arguments(self,parser):
        parser.add_argument("--amount", type=int, help="The number of items that should be created.")
    def handle(self, *args, **options):
        types = list(ExpenseSubCategory.objects.all())
        
        amount = options["amount"] if options["amount"] else 500

        account = Account.objects.get(id=40)
        for i in range(0,amount):
            dt = pytz.utc.localize(datetime.now() - timedelta(days = random.randint(0 , 1825)))
            expense = Item.objects.create(
                account = account,
                item_name = str(f'item {i}'),
                price = i * 20,
                subcategory = random.choice(types)
            )
            expense.created = dt
            expense.save()

        self.stdout.write(self.style.SUCCESS("Successfully populated the database."))

