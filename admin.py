# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import Message


class MessageAdmin(admin.ModelAdmin):
    actions = None
    model = Message
    readonly_fields = ("sender", "receiver", "body", "status", "date")
    list_display = ("sender_view", "receiver_view", "body", "status", "date")
    list_filter = ("sender", "receiver", "status", "date")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def sender_view(self, obj):
        if obj.sender.last_name + obj.sender.first_name == '':
            return obj.sender.username
        else:
            return obj.sender.last_name + ' ' + obj.sender.first_name
        return obj.sender.username
    sender_view.admin_order_field = 'sender__username'
    sender_view.short_description = 'Отправитель'

    def receiver_view(self, obj):
        if obj.receiver.last_name + obj.receiver.first_name == '':
            return obj.receiver.username
        else:
            return obj.receiver.last_name + ' ' + obj.receiver.first_name
    receiver_view.admin_order_field = 'receiver__username'
    receiver_view.short_description = 'Получатель'

admin.site.register(Message, MessageAdmin)
