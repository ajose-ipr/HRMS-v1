from django import forms
from .models import SiteVisit, Expense


class SiteVisitForm(forms.ModelForm):
    class Meta:
        model = SiteVisit
        fields = ['project', 'site_name', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'flat-date oh-input', 'autocomplete': 'off'}),
            'end_date': forms.TextInput(attrs={'class': 'flat-date oh-input', 'autocomplete': 'off'}),
            'site_name': forms.TextInput(attrs={'class': 'oh-input'}),
            'description': forms.Textarea(attrs={'class': 'oh-input', 'rows': 3}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'description', 'estimated_cost']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'flat-date oh-input', 'autocomplete': 'off'}),
            'category': forms.Select(attrs={'class': 'oh-input'}),
            'description': forms.Textarea(attrs={'class': 'oh-input', 'rows': 3}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'oh-input'}),
        }


class ActualExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['actual_cost', 'bill']
        widgets = {
            'actual_cost': forms.NumberInput(attrs={'class': 'oh-input'}),
        }
