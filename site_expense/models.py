from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from employee.models import Employee
from project.models import Project  # optional if you want to link to existing projects

class SiteVisit(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    site_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.site_name} ({self.employee})"
    
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("taxi", "Taxi / Travel"),
        ("food", "Food"),
        ("stay", "Stay / Accommodation"),
        ("other", "Other"),
    ]

    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    bill = models.FileField(upload_to="site_expense/bills/%Y/%m/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site_visit} - {self.category} - {self.date}"