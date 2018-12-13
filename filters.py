# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from rest_framework.filters import BaseFilterBackend
import json


class ModelFieldValueFilter(BaseFilterBackend):
    filter_param = 'filter'
    negative_filter = False

    def filter_queryset(self, request, queryset, view):
        filter_params = request.query_params.get(self.filter_param)
        if filter_params:
            if self.negative_filter:
                return queryset.exclude(**json.loads(filter_params))
            return queryset.filter(**json.loads(filter_params))
        return queryset


class ModelFieldValueExclude(ModelFieldValueFilter):
    filter_param = 'exclude'
    negative_filter = True

