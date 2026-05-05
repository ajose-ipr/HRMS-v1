"""
Filters for site gallery app
"""

from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from django.db.models import Q

from site_gallery.models import Photo, Location, Project


class PhotoFilterSet(FilterSet):
    """FilterSet for Photo model"""

    caption = CharFilter(
        field_name="caption",
        lookup_expr="icontains",
    )

    uploader_name = CharFilter(
        method="filter_uploader_name",
    )

    location = ModelChoiceFilter(
        queryset=Location.objects.all(),
    )

    project = ModelChoiceFilter(
        queryset=Project.objects.all(),
    )

    class Meta:
        model = Photo
        fields = ["location", "project", "uploader_name", "caption"]

    def filter_uploader_name(self, queryset, name, value):
        """Filter by uploader username or full name"""
        return queryset.filter(
            Q(uploader__username__icontains=value)
            | Q(uploader__first_name__icontains=value)
            | Q(uploader__last_name__icontains=value)
        )
