# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from app_gisdata import pagination
from . import models, serializers, filters
from django.db import connection
from . import consumers
from django.http import HttpResponse


class MessageViewset(viewsets.ModelViewSet):
    filter_backends = (
        filters.ModelFieldValueFilter,
    )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.MessageSerializer
    queryset = models.Message.objects.all()
    pagination_class = pagination.MainPagination

    def list(self, request, *args, **kwargs):
        without_data = request.query_params.get('without_data') == 'true'
        if without_data:
            return Response(dict(
                status='success',
                count=self.filter_queryset(self.get_queryset()).count(),
                results=[]
            ))
        else:
            response = super(MessageViewset, self).list(
                request, *args, **kwargs)
            response.data = dict(
                status='success',
                count=len(response.data),
                results=response.data
            )
            return response


class IncomingMessageViewset(viewsets.ModelViewSet):
    filter_backends = (
        filters.ModelFieldValueFilter,
    )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.MessageSerializer
    queryset = models.Message.objects.all()
    pagination_class = pagination.MainPagination

    def get_queryset(self):
        queryset = super(IncomingMessageViewset, self).get_queryset()
        return queryset.filter(receiver=self.request.user)

    def list(self, request, *args, **kwargs):
        without_data = request.query_params.get('without_data') == 'true'
        if without_data:
            return Response(dict(
                status='success',
                count=self.filter_queryset(self.get_queryset()).count(),
                results=[]
            ))
        else:
            response = super(IncomingMessageViewset, self).list(
                request, *args, **kwargs)
            response.data = dict(
                status='success',
                count=len(response.data),
                results=response.data
            )
            return response


class OutgoingMessageViewset(viewsets.ModelViewSet):
    filter_backends = (
        filters.ModelFieldValueFilter,
    )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.MessageSerializer
    queryset = models.Message.objects.all()
    pagination_class = pagination.MainPagination

    def get_queryset(self):
        queryset = super(OutgoingMessageViewset, self).get_queryset()
        return queryset.filter(sender=self.request.user)

    def list(self, request, *args, **kwargs):
        without_data = request.query_params.get('without_data') == 'true'
        if without_data:
            return Response(dict(
                status='success',
                count=self.filter_queryset(self.get_queryset()).count(),
                results=[]
            ))
        else:
            response = super(OutgoingMessageViewset, self).list(
                request, *args, **kwargs)
            response.data = dict(
                status='success',
                count=len(response.data),
                results=response.data
            )
            return response

