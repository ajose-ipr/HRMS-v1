from django.urls import path
from . import views

app_name = "site_expense"

urlpatterns = [
    path("my-expenses/", views.my_expenses, name="my-expenses"),
    path("add-visit/", views.add_site_visit, name="add-visit"),
    path("edit-visit/<int:pk>/", views.edit_site_visit, name="edit-visit"),
    path("visit/<int:pk>/", views.visit_detail, name="visit-detail"),
    path("visit/<int:visit_pk>/add-expense/", views.add_expense, name="add-expense"),
    path("expense/<int:pk>/finalize/", views.finalize_expense, name="finalize-expense"),
    path("manager-expenses/", views.manager_expenses, name="manager-expenses"),
    path("monthly-analysis/", views.monthly_analysis, name="monthly-analysis"),
]
