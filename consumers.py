# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from message_store.models import Message
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from fieldsignals import post_save_changed
from app_gisdata import serializers as gisdata_serializer

from threadlocals.threadlocals import get_current_request
from .redis_cli import RedisCli
r = RedisCli.instance()


@receiver(post_save_changed, sender=Message)
def on_change(sender, instance, changed_fields, **kwargs):
    messages = Message.objects.filter(receiver=instance.receiver, status=False)
    message_data = {}
    message_data['incoming'] = {instance.receiver.id: messages.count()}
    to_user = {}
    to_user['id'] = instance.sender_id
    to_user['username'] = instance.sender.username
    to_user['first_name'] = instance.sender.first_name
    to_user['last_name'] = instance.sender.last_name
    to_user['text'] = instance.body
    to_user['date'] = instance.date
    to_user['user_data'] = gisdata_serializer.UserSerializer(instance.sender).data
    to_user['status'] = instance.status
    to_user['obj_id'] = instance.id
    to_user['sender'] = gisdata_serializer.UserSerializer(instance.sender).data
    to_user['receiver'] = gisdata_serializer.UserSerializer(instance.receiver).data
    to_user['receiver_id'] = instance.receiver.id
    to_user['sender_id'] = instance.sender.id

    for item in changed_fields:
        if item.name == 'status':
            to_user['count'] = 0
            to_user['change_status'] = True
            message_data[instance.receiver_id] = {instance.sender_id: to_user}

    else:
        for i in messages:
            to_user['count'] = messages.filter(
                sender=instance.sender, status=False).count()
            to_user['change_status'] = False
            message_data[i.receiver_id] = {instance.sender_id: to_user}        
    r.publish('users', json.dumps(message_data, cls=DjangoJSONEncoder))


def send_update_message(receiver_id, sender_id):
    receiver_id = int(receiver_id)
    sender_id = int(sender_id)
    request = get_current_request()
    messages = Message.objects.filter(receiver=request.user, status=False)
    message_data = {}
    message_data['incoming'] = {receiver_id: messages.count()}
    to_user = {}
    to_user['id'] = receiver_id
    to_user['count'] = 0
    message_data[receiver_id] = {sender_id: to_user}
    r.publish('users', json.dumps(message_data, cls=DjangoJSONEncoder))
