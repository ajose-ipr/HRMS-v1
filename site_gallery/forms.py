"""
Forms for site gallery feature
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from site_gallery.models import Location, Photo, Project


class LocationForm(forms.ModelForm):
    """Form for creating/editing locations"""

    class Meta:
        model = Location
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "oh-input",
                    "placeholder": _("Enter location name"),
                }
            ),
        }


class ProjectForm(forms.ModelForm):
    """Form for creating/editing projects"""

    class Meta:
        model = Project
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "oh-input",
                    "placeholder": _("Enter project name"),
                }
            ),
        }


class PhotoForm(forms.ModelForm):
    """Form for uploading and editing photos"""

    location_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "oh-input",
                "placeholder": _("Select or create location"),
                "list": "locations_list",
            }
        ),
        label=_("Location"),
    )

    project_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "oh-input",
                "placeholder": _("Select or create project"),
                "list": "projects_list",
            }
        ),
        label=_("Project"),
    )

    class Meta:
        model = Photo
        fields = ["image", "location", "project", "caption"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "oh-input",
                    "accept": "image/*",
                }
            ),
            "location": forms.Select(
                attrs={
                    "class": "oh-select oh-select--sm",
                }
            ),
            "project": forms.Select(
                attrs={
                    "class": "oh-select oh-select--sm",
                }
            ),
            "caption": forms.Textarea(
                attrs={
                    "class": "oh-input",
                    "rows": 3,
                    "placeholder": _("Enter a caption (optional)"),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["location"].required = False
        self.fields["project"].required = False
        self.fields["caption"].required = False


class PhotoFilterForm(forms.Form):
    """Form for filtering photos"""

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "oh-select oh-select--sm",
            }
        ),
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "oh-select oh-select--sm",
            }
        ),
    )

    uploader = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "oh-input",
                "placeholder": _("Filter by uploader"),
            }
        ),
    )
