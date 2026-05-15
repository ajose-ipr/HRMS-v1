from django.urls import path
from . import views

app_name = "site_expense"

urlpatterns = [
    path("my-expenses/", views.my_expenses, name="my-expenses"),
    path("manager-expenses/", views.manager_expenses, name="manager-expenses"),
    path("monthly-analysis/", views.monthly_analysis, name="monthly-analysis"),
]