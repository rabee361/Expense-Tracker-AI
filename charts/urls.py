from django.urls import path
from .views import *

urlpatterns = [
    path('items/' , ListItemsView.as_view()),
    path('create-item/', CreateItemView.as_view()),
    path('get-item/<str:pk>/' , GetItemView.as_view()),
    path('delete-item/<str:pk>/' , DeleteItemView.as_view()),
    path('update-item/<str:pk>/' , UpdateItemView.as_view()),

    path('subcategories/' , ListCreateSubCategory.as_view()),
    path('create-subcategory/' , ListCreateSubCategory.as_view()),
    path('get-subcategory/<str:pk>/' , RetUpdDesSubCategory.as_view()),
    path('pie-subcategories/' , PieChartSubCategory.as_view()),

    path('categories/' , ListCreateCategory.as_view()),
    path('create-category/' , ListCreateCategory.as_view()),
    path('get-category/<str:pk>/' , RetUpdDesCategory.as_view()),
    path('pie-categories/' , PieChartCategories.as_view()),

    path('line-chart/<str:year>/' , LineChart.as_view()),

    path('upcoming-payments/' , ListCreateUpcomingPayment.as_view()),
    path('get-upcoming-payment/<str:pk>/' ,RetUpdDesUpcomingPayment.as_view()),

    path('list-goals/' , ListSavingGoal.as_view()),
    path('create-goal/' , CreateSavingGoal.as_view()),
    path('get-goal/<str:pk>/' , RetUpdDesSavingsGoal.as_view()),
    path('update-goal/<str:pk>/' , RetUpdDesSavingsGoal.as_view()),
    path('delete-goal/<str:pk>/' , RetUpdDesSavingsGoal.as_view()),
    path('add-goal-payment/' , AddGoalPayment.as_view()),

    path('list-limits/' , ListCreateLimits.as_view()),
    path('create-limit/' , ListCreateLimits.as_view()),
    path('get-limit/<str:pk>' , RetUpdDesLimit.as_view()),
    path('update-limit/<str:pk>' , RetUpdDesLimit.as_view()),
    path('delete-limit/<str:pk>' , RetUpdDesLimit.as_view()),

]     