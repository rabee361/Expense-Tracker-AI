from rest_framework import serializers
from .models import *
from utils.helper import *
import calendar



class ItemsPerMonthSerializer(serializers.Serializer):
    month_name = serializers.SerializerMethodField()
    sum = serializers.IntegerField()

    def get_month_name(self, obj):
        return calendar.month_name[obj['month']]
    


class GroupCategoriesSerializer(serializers.Serializer):
    category = serializers.CharField(source='subcategory__category__name')
    sum = serializers.IntegerField()



class GroupSubCategoriesSerializer(serializers.Serializer):
    subcategory = serializers.CharField(source='subcategory__name')
    sum = serializers.IntegerField()



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSubCategory
        fields = '__all__'



class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='subcategory.category.name',read_only=True)
    category_icon = serializers.ImageField(source='subcategory.category.icon',read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name',read_only=True)
    subcategory_icon = serializers.ImageField(source='subcategory.icon',read_only=True)

    class Meta:
        model = Item
        fields = '__all__'




class UpcomingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingPayment
        fields = '__all__'        




class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        exclude = ['user']

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        validated_data['user'] = CustomUser.objects.get(id=user_id)
        return SavingsGoal.objects.create(**validated_data)
         
        
    

class SpendingLimitSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name',read_only=True)
    current_spending = serializers.SerializerMethodField()

    class Meta:
        model = SpendingLimit
        fields = '__all__'
    
    def get_current_spending(self,obj):
        return obj.current_spending

    # def create(self, validated_data):
    #     category_name = validated_data.pop('category_name')
    #     category = ExpenseCategory.objects.get(name=category_name)
    #     validated_data['category'] = category
    #     return super().create(validated_data)
