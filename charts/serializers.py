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
         
        
    