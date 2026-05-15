from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from horilla.methods import handle_no_permission
from site_expense.models import Expense, SiteVisit
from site_expense.forms import SiteVisitForm, ExpenseForm


@login_required
def my_expenses(request):
    employee = request.user.employee_get
    visits = SiteVisit.objects.filter(employee=employee).order_by("-start_date")
    return render(request, "site_expense/my_expenses.html", {"visits": visits})


@login_required
def add_site_visit(request):
    employee = request.user.employee_get
    form = SiteVisitForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        visit = form.save(commit=False)
        visit.employee = employee
        visit.save()
        messages.success(request, "Site visit added successfully.")
        return redirect("site_expense:my-expenses")
    return render(request, "site_expense/add_site_visit.html", {"form": form})


@login_required
def edit_site_visit(request, pk):
    employee = request.user.employee_get
    visit = get_object_or_404(SiteVisit, pk=pk, employee=employee)
    form = SiteVisitForm(request.POST or None, instance=visit)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Site visit updated.")
        return redirect("site_expense:my-expenses")
    return render(request, "site_expense/add_site_visit.html", {"form": form, "edit": True})


@login_required
def add_expense(request, visit_pk):
    employee = request.user.employee_get
    visit = get_object_or_404(SiteVisit, pk=visit_pk, employee=employee)
    form = ExpenseForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.site_visit = visit
        expense.save()
        messages.success(request, "Expense added successfully.")
        return redirect("site_expense:visit-detail", pk=visit_pk)
    return render(request, "site_expense/add_expense.html", {"form": form, "visit": visit})


@login_required
def visit_detail(request, pk):
    employee = request.user.employee_get
    visit = get_object_or_404(SiteVisit, pk=pk, employee=employee)
    expenses = visit.expenses.all().order_by("date")
    return render(request, "site_expense/visit_detail.html", {"visit": visit, "expenses": expenses})


@login_required
def manager_expenses(request):
    manager = request.user.employee_get
    if not manager.reporting_manager.exists() and not manager.get_subordinate_employees():
        return handle_no_permission(request)

    visits = SiteVisit.objects.filter(
        Q(employee__employee_work_info__reporting_manager_id=manager)
        | Q(employee=manager)
    ).order_by("-start_date")
    return render(request, "site_expense/manager_expenses.html", {"visits": visits})


@login_required
def monthly_analysis(request):
    employee = request.user.employee_get
    data = (
        Expense.objects.filter(site_visit__employee=employee)
        .annotate(month=TruncMonth("date"))
        .values("month", "category")
        .annotate(total_estimated=Sum("estimated_cost"), total_actual=Sum("actual_cost"))
        .order_by("-month")
    )
    return render(request, "site_expense/monthly_analysis.html", {"data": data})
