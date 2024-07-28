from rest_framework.views import APIView
from .serializers import *
from .models import Item 
from rest_framework.response import Response
from utils.helper import *
from django.db.models import Sum , F , Q
from django.db.models.functions import ExtractMonth
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView , GenericAPIView , RetrieveUpdateDestroyAPIView , RetrieveAPIView , UpdateAPIView , DestroyAPIView , ListAPIView
from project.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status


class ListItemsView(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(id=self.request.user.id)
        category = ExpenseCategory.objects.get(name=self.request.data['name'])
        serializer.save(client=user, category=category)







class CreateItemView(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(id=self.request.user.id)
        # subcategory = ExpenseSubCategory.objects.get(name=self.request.data['expense_type'])
        serializer.save(client=user)

    def get_queryset(self):
        date = timezone.now().today()
        return Item.objects.filter(created__date=date)
    




class GetItemView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    

class DeleteItemView(DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)



class UpdateItemView(UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    


class ListCreateCategory(ListCreateAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]



class RetUpdDesCategory(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = CategorySerializer




class ListCreateSubCategory(ListCreateAPIView):
    queryset = ExpenseSubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend]




class RetUpdDesSubCategory(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseSubCategory.objects.all()
    serializer_class = SubCategorySerializer




class ListCreateUpcomingPayment(ListCreateAPIView):
    queryset = UpcomingPayment.objects.all()
    serializer_class = UpcomingPaymentSerializer



class RetUpdDesUpcomingPayment(RetrieveUpdateDestroyAPIView):
    queryset = UpcomingPayment.objects.all()
    serializer_class = UpcomingPaymentSerializer







class CreateSavingGoal(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = SavingsGoalSerializer(data=request.data , context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




class RetUpdDesSavingsGoal(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SavingsGoal.objects.all()
    serializer_class = SavingsGoalSerializer
        



class ListSavingGoal(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SavingsGoal.objects.all()
    serializer_class = SavingsGoalSerializer

    def get_queryset(self):
        user = self.request.user
        goals = SavingsGoal.objects.filter(user__id=user.id)
        return goals




class AddGoalPayment(APIView):
    permission_classes = [IsAuthenticated]
        
    def post(self,request):
        payment = request.data.get('payment',None)
        id = request.data.get('goal_id',None)
        if isinstance(payment, int) and isinstance(id, int):
            try:
                saving_goal = SavingsGoal.objects.get(user=request.user,id=id)
                saving_goal.add_payment(payment)
                serializer = SavingsGoalSerializer(saving_goal)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except SavingsGoal.DoesNotExist:
                return Response({"error":"لا يوجد هدف بهذه المعلومات"} , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"أدخل قيمة رقمية صحيحة"} , status=status.HTTP_400_BAD_REQUEST)





class PieChartCategories(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter

    def get(self,request,account_id):
        account = Account.objects.get(id=account_id)
        if request.user != account.user:
            return Response({"error" : "you are not allowed in this account"} ,status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(Item.objects.filter(account=account_id))
        grouped_expenses = queryset.values("subcategory__category__name")\
                                    .annotate(sum=Sum("price"))\
                                    .values("subcategory__category__name","sum").distinct()
        serializer = GroupCategoriesSerializer(grouped_expenses, many=True)
        return Response(serializer.data)



class PieChartSubCategory(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter

    def post(self,request,account_id):
        category = request.data['category']
        account = Account.objects.get(id=account_id)
        if request.user != account.user:
            return Response({"error" : "you are not allowed in this account"} ,status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.filter_queryset(Item.objects.filter(Q(user=request.user)&Q(subcategory__category__name=category)))
        grouped_expenses = queryset.values("subcategory__category__name")\
                                    .annotate(sum=Sum("price"))\
                                    .values("subcategory__category__name","sum").distinct()
        serializer = GroupCategoriesSerializer(grouped_expenses, many=True)
        return Response(serializer.data)



class LineChart(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request, year):
        grouped_expenses = Item.objects.filter(Q(created=year)&Q(user=self.request.user)).\
                                        annotate(item_price=F("price")).\
                                        annotate(month=ExtractMonth("created")).\
                                        values("month").annotate(sum=Sum("price")).\
                                        values("month", "sum").order_by("month")
        serializer = ItemsPerMonthSerializer(grouped_expenses, many=True)
        return Response(serializer.data)






class ListCreateLimits(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = SpendingLimit.objects.all()
    serializer_class = SpendingLimitSerializer
        



class RetUpdDesLimit(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = SpendingLimit.objects.all()
    serializer_class = SpendingLimitSerializer
        
