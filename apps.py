# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class MessageStoreConfig(AppConfig):
    name = 'message_module'
    verbose_name = "Сообщения"

    def ready(self):
        import consumers
