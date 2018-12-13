# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from . import models
from app_gisdata import serializers as gisdata_serializer


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = '__all__'

    def to_representation(self, instance):
        representation_data = {}
        representation_data["id"] = instance.pk
        representation_data["sender"] = gisdata_serializer.UserSerializer(instance.sender).data
        representation_data["receiver"] = gisdata_serializer.UserSerializer(instance.receiver).data
        representation_data["body"] = "{}".format(instance.body)
        representation_data["status"] = instance.status
        representation_data["date"] = instance.date
        representation_data["sender_id"] = instance.sender.id
        representation_data["receiver_id"] = instance.receiver.id
        return representation_data
