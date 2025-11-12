from django_filters import rest_framework as filters
from main.models import Problem

class ProblemFilter(filters.FilterSet):

    class Meta:
        model = Problem
        fields = ['difficulty', 'tags']
